resource "aws_ecs_cluster" "dialog_bot_cluster" {
  name = "dialog-bot"
}

resource "aws_ecs_task_definition" "dialog_bot_task" {
  family                   = "dialog-bot-task"
  container_definitions    = jsonencode([
    {
      "name": "dialog-bot-task",
      "image": "227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80
        },
        {
          "containerPort": 443,
          "hostPort": 443
        }
      ],
      "memory": 512,
      "cpu": 256
    }
  ])
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  memory                   = 512
  cpu                      = 256
  execution_role_arn       = "${aws_iam_role.ecsTaskExecutionRole.arn}"
}

resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = "${data.aws_iam_policy_document.assume_role_policy.json}"
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = "${aws_iam_role.ecsTaskExecutionRole.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

#resource "aws_vpc" "dialog_bot_vpc" {
#  cidr_block           = "10.123.0.0/16"
#  enable_dns_hostnames = true
#  enable_dns_support   = true
#}

#resource "aws_subnet" "dialog_bot_subnet" {
#  vpc_id                  = aws_vpc.dialog_bot_vpc.id
#  cidr_block              = "10.123.1.0/24"
#  map_public_ip_on_launch = true
#  availability_zone       = "eu-west-2"
#}

#resource "aws_internet_gateway" "dialog_bot_gateway" {
#  vpc_id = aws_vpc.dialog_bot_vpc.id
#}

#resource "aws_route_table" "dialog_bot_route_table" {
#  vpc_id = aws_vpc.dialog_bot_vpc.id
#}

#resource "aws_route" "dialog_bot_route" {
#  route_table_id         = aws_route_table.dialog_bot_route_table.id
#  destination_cidr_block = "0.0.0.0/0"
#  gateway_id             = aws_internet_gateway.dialog_bot_gateway.id
#}

#resource "aws_route_table_association" "dialog_bot_route_table_association" {
#  subnet_id      = aws_subnet.dialog_bot_subnet.id
#  route_table_id = aws_route_table.dialog_bot_public_route_table.id
#}

#resource "aws_security_group" "dialog_bot_security_group" {
#  name        = "dialog_bot_security_group"
#  description = "dialog bot security group"
#  vpc_id      = aws_vpc.dialog_bot_vpc.id

#  ingress {
#    from_port   = 0
#    to_port     = 0
#    protocol    = "-1"
#    cidr_blocks = ["*.*.*.*/32"]
#  }

#  egress {
#    from_port   = 0
#    to_port     = 0
#    protocol    = "-1"
#    cidr_blocks = ["0.0.0.0/0"] 
#  }
#}

#resource "aws_instance" "dialog_bot" {
#  instance_type          = "t2.nano"
#  vpc_security_group_ids = [aws_security_group.dialog_bot_security_group.id]
#  subnet_id              = aws_subnet.dialog_bot_subnet.id

#  root_block_device {  
#    volume_size = 20
#  }
#}

