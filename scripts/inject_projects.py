from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.db.models import Agent, Task, Project
from datetime import datetime, timedelta
import random

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    # Clear old tasks & projects (KEEP agents!)
    db.query(Task).delete()
    db.query(Project).delete()
    db.commit()

    # Ensure agents exist
    agents_to_create = [
        'nova', 'flux_main', 'cortexia', 'nero', 'forge',
        'sora', 'daxio', 'enki', 'vondra', 'nura', 'solis', 'vector'
    ]
    
    for agent_id in agents_to_create:
        existing = db.query(Agent).filter(Agent.agent_id == agent_id).first()
        if not existing:
            agent = Agent(
                agent_id=agent_id,
                layer='sentinel' if agent_id not in ['nova', 'flux_main'] else agent_id,
                status='ACTIVE',
                model='claude-3.5-sonnet'
            )
            db.add(agent)
    db.commit()

    # Create 5 projects
    projects = [
        Project(
            project_id="PROJ-alpha",
            name="Project Alpha",
            status="ACTIVE",
            progress=45,
            budget=10000.0,
            spent=4500.0,
            lead_agent="cortexia",
            deadline=datetime.utcnow() + timedelta(days=30)
        ),
        Project(
            project_id="PROJ-beta",
            name="Project Beta",
            status="ACTIVE",
            progress=62,
            budget=15000.0,
            spent=9300.0,
            lead_agent="sora",
            deadline=datetime.utcnow() + timedelta(days=20)
        ),
        Project(
            project_id="PROJ-gamma",
            name="Project Gamma",
            status="ACTIVE",
            progress=28,
            budget=8000.0,
            spent=2240.0,
            lead_agent="vondra",
            deadline=datetime.utcnow() + timedelta(days=45)
        ),
        Project(
            project_id="PROJ-delta",
            name="Project Delta",
            status="ACTIVE",
            progress=81,
            budget=12000.0,
            spent=9720.0,
            lead_agent="solis",
            deadline=datetime.utcnow() + timedelta(days=10)
        ),
        Project(
            project_id="PROJ-epsilon",
            name="Project Epsilon",
            status="PAUSED",
            progress=15,
            budget=6000.0,
            spent=900.0,
            lead_agent="nero",
            deadline=datetime.utcnow() + timedelta(days=60)
        ),
    ]

    for project in projects:
        db.add(project)
    db.commit()

    # Create tasks per project
    agent_list = agents_to_create
    
    task_count = 1
    for project in projects:
        num_tasks = random.randint(8, 15)
        
        for i in range(num_tasks):
            task_status = random.choices(
                ['CREATED', 'IN_PROGRESS', 'COMPLETED'],
                weights=[40, 40, 20]
            )[0]
            
            assigned_agent = None
            if task_status in ['IN_PROGRESS', 'COMPLETED']:
                assigned_agent = random.choice(agent_list)
            
            task = Task(
                task_id=f"TASK-{task_count:04d}",
                status=task_status,
                agent_id=assigned_agent,
                project_id=project.project_id,
                priority=random.choice(['LOW', 'NORMAL', 'HIGH']),
            )
            db.add(task)
            task_count += 1
    
    db.commit()
    print("✅ Projects & Tasks injected successfully!")
    print(f"   - 5 projects created")
    print(f"   - {task_count - 1} tasks created")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
