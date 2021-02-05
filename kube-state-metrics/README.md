## 一、Metrics Server 介绍
`Metrics Server`是kubernetes集群核心监控数据的聚合器，可以通过`Metrics API`的形式获取`Metrics`数据

**注意：**  
`Metrics Server`只获取指标的最新值，不对旧值进行存储，且不负责将指标转发到第三方目标

## 二、使用帮助
```bash
kubectl apply -f 01-rbac.yaml -n kube-system
kubectl apply -f 02-api-svc.yaml -n kube-system
kubectl apply -f 02-svc.yaml -n kube-system
kubectl apply -f 03-deployment.yaml -n kube-system
```
