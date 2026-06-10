# 二手循环商店 API

```bash
cp .env.example .env
docker compose up -d --build
```

二手循环商店 API 支持闲置商品发布、搜索购买、交易管理、环保积分、评价信用、消息通知和平台统计。

## 项目主要功能

- 二手商品发布、上下架、库存标记和图片字段。
- PostgreSQL 全文搜索，支持分类、价格、成色和排序。
- 购物车、批量下单和订单状态流转。
- 按重量和类别计算环保积分，支持优惠券兑换记录。
- 交易互评、好评率和信用等级计算。
- 系统通知已读/未读管理。
- 日/周/月交易量、交易额和热门分类统计。

## 本地开发

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

API 文档地址（DRF Browsable API）：http://localhost:19413/api/

## 技术栈

| 类型 | 技术 |
| --- | --- |
| 后端 | Django + Django REST Framework |
| 数据库 | PostgreSQL |
| 认证 | djangorestframework-simplejwt |
| 搜索 | SearchVector + SearchRank |
| 存储 | Django media |

## 目录结构

```text
.
├── backend
│   ├── app
│   │   ├── apps
│   │   ├── constants
│   │   └── utils
│   └── manage.py
├── database
│   └── init.sql
└── docker-compose.yml
```

## 主要 API

- `GET /api/products/` 商品搜索
- `POST /api/products/` 发布商品
- `POST /api/orders/cart/` 加入购物车
- `POST /api/orders/checkout/` 批量下单
- `PATCH /api/orders/{id}/status/` 更新订单状态
- `GET /api/points/summary/` 环保积分汇总
- `POST /api/reviews/` 创建互评
- `GET /api/notifications/` 通知列表
- `GET /api/stats/trades/` 交易统计

## 环境变量说明

| 变量 | 说明 |
| --- | --- |
| `COMPOSE_PROJECT_NAME` | Compose 项目名，默认 `cycleapi` |
| `POSTGRES_*` | PostgreSQL 数据库配置 |
| `DJANGO_SECRET_KEY` | Django 密钥 |
| `DJANGO_DEBUG` | 调试模式 |

## License

MIT
