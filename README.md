# AWS Toolbox

A command-line tool for managing and inspecting AWS resources using boto3.

## Features

- **S3 Operations**: List all S3 buckets and calculate their storage sizes
- **EC2 Operations**: List all EC2 instances across all AWS regions and availability zones
- **EBS Operations**: List all EBS volumes (attached and detached) across all AWS regions

## Installation

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) installed
- AWS credentials configured (via `aws configure`, environment variables, or IAM role)

### Install from source

```bash
git clone <repository-url>
cd aws_toolbox
uv add -r requirements.txt
uv sync
```

## Usage

You can also run the scripts directly with uv:

```bash
# S3 operations
uv run python main.py -ls3

# EC2 operations
uv run python main.py -ec2

# EBS operations
uv run python main.py -ebs
```

## Project Structure

```
aws_boto3/
├── main.py           # Main CLI entry point (S3 + EC2)
├── src/aws_boto3/    # Package (minimal, for distribution)
├── pyproject.toml    # Project configuration
├── requirements.txt  # Dependencies
└── README.md
```

## Dependencies

- **boto3** - AWS SDK for Python
- **argparse** - Command-line argument parsing

## Configuration

Ensure your AWS credentials are configured:

```bash
aws configure
```

Or set environment variables:

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

## Development

### Running tests

Currently no formal test suite exists. Test manually:

```bash
uv run python main.py -ls3
uv run python main.py -ec2
uv run python main.py -ebs
```

### Code style

Follow standard Python conventions (PEP 8). Consider using with uv:
- `uv run ruff check` for linting
- `uv run black` for formatting
- `uv run mypy` for type checking

## License

MIT License

## Author

**Daniel Aslan**  
DevOps Engineer
