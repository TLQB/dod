# DOD (Django on Docker) API

A Django REST API service deployed on Fly.io with PostgreSQL database integration and email functionality.

## Features

- Django 3.2.6 with REST Framework
- JWT Authentication
- PostgreSQL Database
- Email Integration (Zoho SMTP)
- Excel File Processing
- Docker Containerization
- Fly.io Deployment
- Vietnamese Language Support
- Asia/Ho_Chi_Minh Timezone

## Prerequisites

- Docker & Docker Compose
- Python 3.7+
- PostgreSQL

## Installation & Running

dod/local/readme.md

### Code Style

Follow PEP 8 guidelines for Python code style.

## Project Structure

dod/
├── app/
│ ├── app_config/
│ │ ├── settings.py
│ │ └── urls.py
│ ├── api/
│ └── manage.py
├── docker/
├── docker-compose.yml
├── fly.toml
└── README.md

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email dod@powake.dev
