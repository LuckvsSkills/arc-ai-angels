from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.db.models import Agent, Task, Project
from datetime import datetime, timedelta
import random

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    # 1. CREATE ALL AGENTS
    agents_data = [
        ('nova', 'nova'), ('flux_main', 'flux'),
        ('cortexia', 'omni'), ('nero', 'sentinel'), ('forge', 'sentinel'),
        ('sora', 'sentinel'), ('daxio', 'sentinel'), ('enki', 'sentinel'),
        ('vondra', 'sentinel'), ('nura', 'sentinel'),
        ('solis', 'sentinel'), ('vector', 'sentinel'),
    ]
    
    for agent_id, layer in agents_data:
        existing = db.query(Agent).filter(Agent.agent_id == agent_id).first()
        if not existing:
            agent = Agent(agent_id=agent_id, layer=layer, status='ACTIVE', model='claude-3.5-sonnet')
            db.add(agent)
    db.commit()
    print("✅ 12 Agents created")

    # 2. CREATE 5 PROJECTS
    projects = [
        Project(project_id="PROJ-alpha", name="Project Alpha", status="ACTIVE", progress=45, budget=10000.0, spent=4500.0, lead_agent="cortexia", deadline=datetime.utcnow() + timedelta(days=30)),
        Project(project_id="PROJ-beta", name="Project Beta", status="ACTIVE", progress=62, budget=15000.0, spent=9300.0, lead_agent="sora", deadline=datetime.utcnow() + timedelta(days=20)),
        Project(project_id="PROJ-gamma", name="Project Gamma", status="ACTIVE", progress=28, budget=8000.0, spent=2240.0, lead_agent="vondra", deadline=datetime.utcnow() + timedelta(days=45)),
        Project(project_id="PROJ-delta", name="Project Delta", status="ACTIVE", progress=81, budget=12000.0, spent=9720.0, lead_agent="solis", deadline=datetime.utcnow() + timedelta(days=10)),
        Project(project_id="PROJ-epsilon", name="Project Epsilon", status="PAUSED", progress=15, budget=6000.0, spent=900.0, lead_agent="nero", deadline=datetime.utcnow() + timedelta(days=60)),
    ]
    for project in projects:
        db.add(project)
    db.commit()
    print("✅ 5 Projects created")

    # 3. CREATE TASKS
    agent_list = [a[0] for a in agents_data]
    task_count = 1
    for project in projects:
        num_tasks = random.randint(8, 15)
        for i in range(num_tasks):
            task_status = random.choices(['CREATED', 'IN_PROGRESS', 'COMPLETED'], weights=[40, 40, 20])[0]
            assigned_agent = None if task_status == 'CREATED' else random.choice(agent_list)
            task = Task(task_id=f"TASK-{task_count:04d}", status=task_status, agent_id=assigned_agent, project_id=project.project_id, priority=random.choice(['LOW', 'NORMAL', 'HIGH']))
            db.add(task)
            task_count += 1
    db.commit()
    print(f"✅ {task_count - 1} Tasks created")
    print("\n✅ ALL DATA INITIALIZED!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
