variable "app_version" {
    type = string
}

resource "aws_ecs_cluster" "dialog_bot_cluster" {
  name = "dialog-bot"
}

resource "aws_ecs_task_definition" "dialog_bot_task" {
  family                   = "dialog-bot-task"
  container_definitions    = jsonencode([
    {
      "name": "dialog-bot-task",
      "image": "227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot:${var.app_version}",
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "${aws_cloudwatch_log_group.dialog_bot_log_group.name}",
          "awslogs-region": "eu-west-2",
          "awslogs-stream-prefix": "dialog-bot"
        }
      },
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

resource "aws_default_vpc" "default_vpc" {
}

resource "aws_default_subnet" "default_subnet_a" {
  availability_zone = "eu-west-2a"
}

resource "aws_default_subnet" "default_subnet_b" {
  availability_zone = "eu-west-2b"
}

resource "aws_default_subnet" "default_subnet_c" {
  availability_zone = "eu-west-2c"
}

resource "aws_security_group" "allow_http" {
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

resource "aws_security_group" "allow_https" {
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

resource "aws_ecs_service" "app_service" {
  name            = "dialog-bot-service"
  cluster         = "${aws_ecs_cluster.dialog_bot_cluster.id}"
  task_definition = "${aws_ecs_task_definition.dialog_bot_task.arn}"
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets          = [
        "${aws_default_subnet.default_subnet_a.id}",
        "${aws_default_subnet.default_subnet_b.id}",
        "${aws_default_subnet.default_subnet_c.id}"
    ]
    assign_public_ip = true
    security_groups  = [
        "${aws_security_group.allow_http.id}",
        "${aws_security_group.allow_https.id}"
    ]
  }
}

resource "aws_cloudwatch_log_group" "dialog_bot_log_group" {
  name = "dialog-bot-log-group"
  retention_in_days = 1
}

#resource "aws_cloudwatch_event_rule" "markov_parser" {
#  name                = "markov-parser"
#  schedule_expression = "rate(4 hours)"
#}

#resource "aws_cloudwatch_event_target" "dialog_bot_target" {
#  rule      = aws_cloudwatch_event_rule.markov_parser.name
#  target_id = "dialog-bot-target"
#  arn       = aws_ecs_cluster.dialog_bot_cluster.arn

#  ecs_target {
#    task_count          = 1
#    task_definition_arn = aws_ecs_task_definition.dialog_bot_task.arn
#  }
#}

#resource "aws_cloudwatch_event_rule" "ecs_role" {
#  name = "ecsEventsRole"

#  assume_role_policy = jsonencode({
#    Statement = [
#      {
#        Action = "sts:AssumeRole",
#        Effect = "Allow",
#        Principal = {
#          Service = "events.amazonaws.com"
#        },
#      },
#    ],
#    Version = "2012-10-17"
#  })
#}

#resource "aws_cloudwatch_event_permission" "permission_for_events" {
#  statement_id  = "Allow-CloudWatch-Events"
#  action        = "events:PutEvents"
#  principal     = "events.amazonaws.com"
#}
