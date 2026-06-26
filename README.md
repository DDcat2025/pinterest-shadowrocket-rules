# Pinterest Shadowrocket Rules

Pinterest / P 站分流规则，覆盖 Pinterest 主站、各地区域名、Pinimg 图片/视频资源、Pinterest Ads、Business、Analytics、开发者与通知相关域名。

## Shadowrocket 接入

把下面这一行加入 Shadowrocket 配置，并把最后的 `PINTEREST` 改成你自己的 P 站节点或策略组名称：

```ini
RULE-SET,https://raw.githubusercontent.com/DDcat2025/pinterest-shadowrocket-rules/main/rule/Shadowrocket/Pinterest/Pinterest.list,PINTEREST
```

如果你想让 Pinterest 走直连，把最后改成：

```ini
RULE-SET,https://raw.githubusercontent.com/DDcat2025/pinterest-shadowrocket-rules/main/rule/Shadowrocket/Pinterest/Pinterest.list,DIRECT
```

## 文件

- `rule/Shadowrocket/Pinterest/Pinterest.list`：Shadowrocket 规则列表
- `rule/Shadowrocket/Pinterest/Pinterest_Domain.list`：纯域名列表
- `rule/Mihomo/Pinterest/Pinterest.yaml`：Mihomo / Clash Meta 规则
- `data/pinterest-domains.txt`：手工维护的补充域名

## 测试

Pinterest 本身没有稳定可用的 `/cdn-cgi/trace`，所以不能像 Claude/OpenAI 那样直接用 trace 精准回显 Pinterest 分流出口。

可先测试连通性：

```bash
curl -I --connect-timeout 10 https://www.pinterest.com
```

如果要看默认代理出口：

```bash
curl -s https://icanhazip.com
```

注意：上面这个只代表当前默认代理出口，不一定能证明 Pinterest 命中了专属策略组。更准确的判断方式是看 Shadowrocket 日志里 `pinterest.com` / `pinimg.com` 命中的策略名。

## 更新

仓库会通过 GitHub Actions 每周自动合并上游 `v2fly/domain-list-community` 的 Pinterest 列表，并保留本仓库的手工补充域名。
