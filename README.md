# Terraform

Как инициализировать профиль для Yandex Cloud
## Интерактивно создать себе профиль
```
yc init
```

```
export YC_TOKEN=$(yc iam create-token)
export YC_CLOUD_ID=$(yc config get cloud-id)
export YC_FOLDER_ID=$(yc config get folder-id)
```


Куда смотреть за мануалами

1. https://yandex.cloud/ru/docs/terraform/tutorials/terraform-modules#configure-terraform

2. https://yandex.cloud/ru/docs/tutorials/infrastructure-management/terraform-quickstart#install-terraform

## start terraform

```bash
terraform tmf #test configs
terraform init
terraform plan # before aplly, plan infrastructure
terraform apply
```

##  examination
```bash
yc compute instance list
```