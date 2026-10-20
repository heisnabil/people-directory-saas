"""
Development seed script.

Populates the employees table with plausible test data.
Idempotent: checks for existing records by email before inserting,
so it can be run multiple times without creating duplicates.

Usage:
    python -m app.seed
"""

import logging
import sys
from datetime import date

from sqlalchemy.orm import Session

from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.employee import Employee

setup_logging()
logger = logging.getLogger(__name__)

SEED_EMPLOYEES = [
    {
        "name": "Rahul Sharma",
        "email": "rahul.sharma@company.com",
        "department": "Engineering",
        "designation": "Senior Software Engineer",
        "date_of_joining": date(2021, 3, 15),
    },
    {
        "name": "Priya Patel",
        "email": "priya.patel@company.com",
        "department": "Engineering",
        "designation": "Frontend Developer",
        "date_of_joining": date(2022, 7, 1),
    },
    {
        "name": "Amit Kumar",
        "email": "amit.kumar@company.com",
        "department": "Product",
        "designation": "Product Manager",
        "date_of_joining": date(2020, 11, 10),
    },
    {
        "name": "Sneha Reddy",
        "email": "sneha.reddy@company.com",
        "department": "Design",
        "designation": "UI/UX Designer",
        "date_of_joining": date(2023, 1, 20),
    },
    {
        "name": "Vikram Singh",
        "email": "vikram.singh@company.com",
        "department": "Engineering",
        "designation": "DevOps Engineer",
        "date_of_joining": date(2021, 9, 5),
    },
    {
        "name": "Ananya Gupta",
        "email": "ananya.gupta@company.com",
        "department": "Human Resources",
        "designation": "HR Manager",
        "date_of_joining": date(2019, 6, 12),
    },
    {
        "name": "Karthik Nair",
        "email": "karthik.nair@company.com",
        "department": "Engineering",
        "designation": "Backend Developer",
        "date_of_joining": date(2022, 2, 28),
    },
    {
        "name": "Meera Joshi",
        "email": "meera.joshi@company.com",
        "department": "Marketing",
        "designation": "Marketing Analyst",
        "date_of_joining": date(2023, 4, 3),
    },
    {
        "name": "Arjun Desai",
        "email": "arjun.desai@company.com",
        "department": "Finance",
        "designation": "Financial Analyst",
        "date_of_joining": date(2020, 8, 17),
    },
    {
        "name": "Divya Menon",
        "email": "divya.menon@company.com",
        "department": "Engineering",
        "designation": "QA Engineer",
        "date_of_joining": date(2021, 12, 1),
    },
    {
        "name": "Rohan Kapoor",
        "email": "rohan.kapoor@company.com",
        "department": "Product",
        "designation": "Business Analyst",
        "date_of_joining": date(2022, 10, 15),
    },
    {
        "name": "Neha Verma",
        "email": "neha.verma@company.com",
        "department": "Design",
        "designation": "Visual Designer",
        "date_of_joining": date(2023, 6, 22),
    },
    {
        "name": "Siddharth Rao",
        "email": "siddharth.rao@company.com",
        "department": "Engineering",
        "designation": "Tech Lead",
        "date_of_joining": date(2018, 4, 9),
    },
    {
        "name": "Pooja Iyer",
        "email": "pooja.iyer@company.com",
        "department": "Human Resources",
        "designation": "Talent Acquisition",
        "date_of_joining": date(2021, 5, 30),
    },
    {
        "name": "Aditya Bhatt",
        "email": "aditya.bhatt@company.com",
        "department": "Engineering",
        "designation": "Full Stack Developer",
        "date_of_joining": date(2022, 8, 14),
    },
    {
        "name": "Ishita Malhotra",
        "email": "ishita.malhotra@company.com",
        "department": "Marketing",
        "designation": "Content Strategist",
        "date_of_joining": date(2023, 3, 7),
    },
    {
        "name": "Rajesh Khanna",
        "email": "rajesh.khanna@company.com",
        "department": "Finance",
        "designation": "Finance Manager",
        "date_of_joining": date(2017, 10, 25),
    },
    {
        "name": "Kavita Sundaram",
        "email": "kavita.sundaram@company.com",
        "department": "Engineering",
        "designation": "Data Engineer",
        "date_of_joining": date(2022, 1, 10),
    },
    {
        "name": "Manish Tiwari",
        "email": "manish.tiwari@company.com",
        "department": "Product",
        "designation": "Product Designer",
        "date_of_joining": date(2021, 7, 19),
    },
    {
        "name": "Lakshmi Narayan",
        "email": "lakshmi.narayan@company.com",
        "department": "Operations",
        "designation": "Operations Manager",
        "date_of_joining": date(2019, 2, 14),
    },
    {
        "name": "Deepak Chauhan",
        "email": "deepak.chauhan@company.com",
        "department": "Engineering",
        "designation": "Mobile Developer",
        "date_of_joining": date(2023, 9, 1),
    },
    {
        "name": "Ritu Saxena",
        "email": "ritu.saxena@company.com",
        "department": "Legal",
        "designation": "Legal Counsel",
        "date_of_joining": date(2020, 5, 20),
    },
    {
        "name": "Gaurav Mehta",
        "email": "gaurav.mehta@company.com",
        "department": "Engineering",
        "designation": "Cloud Architect",
        "date_of_joining": date(2019, 11, 8),
    },
    {
        "name": "Swati Jain",
        "email": "swati.jain@company.com",
        "department": "Design",
        "designation": "Design Lead",
        "date_of_joining": date(2020, 3, 16),
    },
    {
        "name": "Nikhil Agarwal",
        "email": "nikhil.agarwal@company.com",
        "department": "Sales",
        "designation": "Account Executive",
        "date_of_joining": date(2022, 12, 5),
    },
]


def seed_database() -> None:
    """Insert seed employees if they don't already exist (idempotent)."""
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        existing_emails = {
            row[0] for row in db.query(Employee.email).all()
        }

        new_employees = [
            Employee(**emp_data)
            for emp_data in SEED_EMPLOYEES
            if emp_data["email"] not in existing_emails
        ]

        if new_employees:
            db.add_all(new_employees)
            db.commit()
            logger.info("Seeded %d new employees", len(new_employees))
        else:
            logger.info("All seed employees already exist — nothing to insert")

    except Exception:
        db.rollback()
        logger.exception("Failed to seed database")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
