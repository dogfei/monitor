## 二、使用帮助
因为要持久化数据，所以使用的localstorageclass，需要事先去对应的节点上创建好目录，然后再去执行  

**注意：**  
服务会调度到此节点上

```bash
kubectl apply -f LocalStorageClass/
```
启动服务
```bash
kubectl apply -f 01-ns.yaml
kubectl apply -f 02-rbac.yaml
kubectl apply -f 03-configmap.yaml
kubectl apply -f 04-file-sd-config.yaml
kubectl apply -f 04-rules.yaml
kubectl apply -f 05-svc.yaml
kubectl apply -f 06-deployment.yaml
```