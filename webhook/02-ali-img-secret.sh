kubectl create secret docker-registry ali-img-secret \
  --docker-server=镜像地址 \
  --docker-username=用户名 \
  --docker-password=密码 \
  -n monitoring