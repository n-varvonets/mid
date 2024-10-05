provider "aws" {}

# Эти имена служат только для удобства и ясности кода, чтобы однозначно ссылаться на конкретные блоки данных.
# Они помогают сделать код более читаемым и понятным.
# Например:
# - "working" помогает понять, что данный блок связан с доступными рабочими зонами (availability zones).
# - "current" указывает на текущий контекст вызова, представляя данные о текущей учетной записи.
data "aws_availability_zones" "working" {}
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_vpcs" "my_vpcs" {}

output "aws_vpcs" {
  value = data.aws_vpcs.my_vpcs.ids
}

output "data_aws_availability_zones" {
  value = data.aws_availability_zones.working.names
}

output "data_aws_caller_identity" {
  value = data.aws_caller_identity.current.account_id
}

output "data_aws_region_name" {
  value = data.aws_region.current.name
}

output "data_aws_region_description" {
  value = data.aws_region.current.description
}

# --------------- Так же можно фильтровать по ТЕГАМ -------------
# нужен инстанс с тегом прод
# data "aws_vpc" "prod_vpc" {
#   tags = {
#     Name = "prod"
#   }
# }
#
# output "prod_vpc_id" {
#   value = data.aws_vpc.prod_vpc.id
# }
#
# output "prod_vpc_cidr" {
#   value = data.aws_vpc.prod_vpc.cidr_block
# }

# --------------- Используем в коде ресурсі авс -------------

resource "aws_subnet" "prod_subnet_1" {
  vpc_id            = data.aws_vpc.prod_vpc.id
  availability_zone = data.aws_availability_zones.working.names[0]
  cidr_block        = "10.10.1.0/24"

  tags = {
    Name    = "Subnet-1 in ${data.aws_availability_zones.working.names[0]}"
    Account = "Subnet in Account ${data.aws_caller_identity.current.account_id}"
    Region  = data.aws_region.current.description
  }
}



