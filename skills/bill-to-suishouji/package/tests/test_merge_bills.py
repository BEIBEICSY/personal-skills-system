import unittest

from scripts.merge_bills import filter_clean_records, normalize_alipay_row, normalize_wechat_row


class MergeBillsRefundRulesTest(unittest.TestCase):
    def test_supported_alipay_investment_purchases_are_kept_as_transfers(self):
        products = [
            "蚂蚁财富-广发纳斯达克100ETF联接(QDII)A-买入",
            "南方上海金ETF联接C-买入",
        ]
        records = [
            normalize_alipay_row(
                {
                    "交易时间": f"2026-08-{21-index:02d} 10:23:25",
                    "交易分类": "投资理财",
                    "交易对方": "蚂蚁（杭州）基金销售有限公司",
                    "商品说明": product,
                    "收/支": "不计收支",
                    "金额": "5.00",
                    "收/付款方式": "交通银行储蓄卡(8984)",
                    "交易状态": "交易成功",
                    "交易订单号": f"investment-{index}",
                    "商家订单号": "",
                    "备注": "",
                },
                index,
            )
            for index, product in enumerate(products, start=1)
        ]

        kept, excluded = filter_clean_records(records)

        self.assertEqual(excluded, [])
        self.assertEqual([row["收/支"] for row in kept], ["转账", "转账"])

    def test_unconfigured_alipay_investment_purchase_remains_excluded(self):
        record = normalize_alipay_row(
            {
                "交易时间": "2026-08-21 10:23:25",
                "交易分类": "投资理财",
                "交易对方": "蚂蚁财富",
                "商品说明": "其他债券基金-买入",
                "收/支": "不计收支",
                "金额": "5.00",
                "收/付款方式": "交通银行储蓄卡(8984)",
                "交易状态": "交易成功",
                "交易订单号": "unconfigured-investment",
                "商家订单号": "",
                "备注": "",
            },
            1,
        )

        kept, excluded = filter_clean_records([record])

        self.assertEqual(kept, [])
        self.assertEqual(excluded[0]["排除原因"], "不计收支/中性交易")

    def test_wechat_full_refund_excludes_refund_and_original_expense(self):
        records = [
            normalize_wechat_row(
                {
                    "交易时间": "2026-06-30 12:31:24",
                    "交易类型": "肯德基-退款",
                    "交易对方": "肯德基",
                    "商品": "肯德基",
                    "收/支": "收入",
                    "金额(元)": "15",
                    "支付方式": "交通银行储蓄卡(8984)",
                    "当前状态": "已全额退款",
                    "交易单号": "refund-order",
                    "商户单号": "",
                    "备注": "/",
                },
                1,
            ),
            normalize_wechat_row(
                {
                    "交易时间": "2026-06-30 12:31:03",
                    "交易类型": "商户消费",
                    "交易对方": "肯德基",
                    "商品": "KFC_PRE_PLUSWX10012647068623968092550",
                    "收/支": "支出",
                    "金额(元)": "15",
                    "支付方式": "交通银行储蓄卡(8984)",
                    "当前状态": "已全额退款",
                    "交易单号": "expense-order",
                    "商户单号": "WX10012647068623968092550",
                    "备注": "/",
                },
                2,
            ),
            normalize_wechat_row(
                {
                    "交易时间": "2026-06-30 10:00:00",
                    "交易类型": "商户消费",
                    "交易对方": "luckin coffee",
                    "商品": "订单付款",
                    "收/支": "支出",
                    "金额(元)": "9.9",
                    "支付方式": "招商银行信用卡(6020)",
                    "当前状态": "支付成功",
                    "交易单号": "kept-order",
                    "商户单号": "merchant-order",
                    "备注": "/",
                },
                3,
            ),
        ]

        kept, excluded = filter_clean_records(records)

        self.assertEqual([row["交易对象"] for row in kept], ["luckin coffee"])
        self.assertEqual({row["交易对象"] for row in excluded}, {"肯德基"})

    def test_alipay_refund_order_reference_excludes_original_expense(self):
        records = [
            normalize_alipay_row(
                {
                    "交易时间": "2026-06-27 14:54:24",
                    "交易分类": "餐饮美食",
                    "交易对方": "美团",
                    "商品说明": "退款-Pinkdoo拼豆",
                    "收/支": "不计收支",
                    "金额": "29.99",
                    "收/付款方式": "余额宝",
                    "交易状态": "退款成功",
                    "交易订单号": "2026062722001464471435537285_20260627145424R2640",
                    "商家订单号": "20260627144826U11425987503287362",
                    "备注": "",
                },
                1,
            ),
            normalize_alipay_row(
                {
                    "交易时间": "2026-06-27 14:48:31",
                    "交易分类": "餐饮美食",
                    "交易对方": "美团",
                    "商品说明": "Pinkdoo拼豆",
                    "收/支": "支出",
                    "金额": "29.99",
                    "收/付款方式": "余额宝",
                    "交易状态": "交易关闭",
                    "交易订单号": "2026062722001464471435537285",
                    "商家订单号": "20260627144826U11425987503287362",
                    "备注": "",
                },
                2,
            ),
            normalize_alipay_row(
                {
                    "交易时间": "2026-06-27 10:00:00",
                    "交易分类": "餐饮美食",
                    "交易对方": "金膳餐饮",
                    "商品说明": "食堂订餐",
                    "收/支": "支出",
                    "金额": "19.00",
                    "收/付款方式": "招商银行信用卡(6020)",
                    "交易状态": "交易成功",
                    "交易订单号": "kept-order",
                    "商家订单号": "kept-merchant",
                    "备注": "",
                },
                3,
            ),
        ]

        kept, excluded = filter_clean_records(records)

        self.assertEqual([row["交易对象"] for row in kept], ["金膳餐饮"])
        self.assertEqual({row["交易对象"] for row in excluded}, {"美团"})

    def test_refund_to_member_income_is_excluded(self):
        records = [
            normalize_alipay_row(
                {
                    "交易时间": "2026-06-07 22:01:15",
                    "交易分类": "转账红包",
                    "交易对方": "支付宝小荷包(因因贝贝出行)",
                    "商品说明": "批量退款给成员",
                    "收/支": "收入",
                    "金额": "126.34",
                    "收/付款方式": "账户余额",
                    "交易状态": "转账成功",
                    "交易订单号": "refund-member",
                    "商家订单号": "member",
                    "备注": "",
                },
                1,
            )
        ]

        kept, excluded = filter_clean_records(records)

        self.assertEqual(kept, [])
        self.assertEqual(excluded[0]["排除原因"], "退款相关")


if __name__ == "__main__":
    unittest.main()
