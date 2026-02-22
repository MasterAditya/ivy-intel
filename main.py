from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from database import engine, SessionLocal, Base
from models import Opportunity, Student, Application, Post, Comment
from helpers import calculate_incoscore, classify_opportunity


def seed_database():
    """Seed the database with initial sample data."""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Opportunity).first() is not None:
            return

        # Seed Ivy League opportunities with auto-classified domains
        opportunity_data = [
            {
                "title": "AI Research Fellowship",
                "description": "Join Harvard's cutting-edge AI research lab to work on machine learning and neural networks.",
                "university": "Harvard",
                "posted_date": date(2026, 2, 15)
            },
            {
                "title": "Data Science Summer Internship",
                "description": "Yale's Data Science Institute offers hands-on experience with big data analytics.",
                "university": "Yale",
                "posted_date": date(2026, 2, 10)
            },
            {
                "title": "Legal Policy Research Program",
                "description": "Princeton's law and policy center seeks students for legal research and policy analysis.",
                "university": "Princeton",
                "posted_date": date(2026, 2, 8)
            },
            {
                "title": "Biomedical Research Assistant",
                "description": "Columbia's biomedical center needs research assistants for clinical health studies.",
                "university": "Columbia",
                "posted_date": date(2026, 2, 5)
            },
            {
                "title": "Robotics Engineering Fellowship",
                "description": "Penn's robotics lab offers engineering and hardware development opportunities.",
                "university": "UPenn",
                "posted_date": date(2026, 1, 28)
            },
            {
                "title": "Quantum Computing Research",
                "description": "MIT's quantum computing lab seeks students for quantum algorithm and quantum machine learning research.",
                "university": "MIT",
                "posted_date": date(2026, 2, 12)
            },
            {
                "title": "Constitutional Law Clinic",
                "description": "Stanford Law School invites students to participate in constitutional law litigation and legal advocacy.",
                "university": "Stanford",
                "posted_date": date(2026, 2, 1)
            },
            {
                "title": "Neuroscience Research Fellowship",
                "description": "Brown's neuroscience department offers clinical brain research and cognitive science studies.",
                "university": "Brown",
                "posted_date": date(2026, 1, 25)
            },
            {
                "title": "Sustainable Engineering Initiative",
                "description": "Cornell's engineering school focuses on renewable energy and sustainable infrastructure development.",
                "university": "Cornell",
                "posted_date": date(2026, 1, 20)
            },
            {
                "title": "Healthcare Informatics Program",
                "description": "Dartmouth's medical school offers healthcare data analytics and medical AI research opportunities.",
                "university": "Dartmouth",
                "posted_date": date(2026, 1, 15)
            }
        ]
        
        opportunities = [
            Opportunity(
                title=data["title"],
                description=data["description"],
                university=data["university"],
                domain=classify_opportunity(data["description"]),
                posted_date=data["posted_date"]
            )
            for data in opportunity_data
        ]

        # Seed students with different metrics
        students = [
            Student(
                name="Alice Chen",
                email="alice@university.edu",
                domain_interest="AI",
                skills="Python, TensorFlow, PyTorch, Machine Learning",
                bio="AI enthusiast passionate about neural networks and deep learning research.",
                hackathons=5,
                internships=2,
                research_papers=1,
                coding_score=92.5
            ),
            Student(
                name="Bob Martinez",
                email="bob@university.edu",
                domain_interest="Law",
                skills="Legal Research, Policy Analysis, Public Speaking",
                bio="Aspiring legal scholar interested in tech policy and intellectual property.",
                hackathons=3,
                internships=1,
                research_papers=0,
                coding_score=85.0
            ),
            Student(
                name="Carol Williams",
                email="carol@university.edu",
                domain_interest="Biomedical",
                skills="R, SPSS, Clinical Research, Data Analysis",
                bio="Pre-med student focused on biomedical informatics and clinical studies.",
                hackathons=2,
                internships=3,
                research_papers=3,
                coding_score=88.0
            ),
            Student(
                name="David Park",
                email="david@university.edu",
                domain_interest="Engineering",
                skills="C++, MATLAB, CAD, Robotics, Embedded Systems",
                bio="Mechanical engineering student with a passion for robotics and automation.",
                hackathons=6,
                internships=2,
                research_papers=2,
                coding_score=90.0
            ),
            Student(
                name="Elena Rodriguez",
                email="elena@university.edu",
                domain_interest="AI",
                skills="Python, NLP, Computer Vision, Deep Learning",
                bio="Graduate researcher specializing in natural language processing and AI ethics.",
                hackathons=4,
                internships=3,
                research_papers=5,
                coding_score=95.0
            ),
            Student(
                name="Frank Thompson",
                email="frank@university.edu",
                domain_interest="Biomedical",
                skills="Biology, Chemistry, Lab Techniques, Medical Research",
                bio="Pre-med student interested in pharmaceutical research and drug discovery.",
                hackathons=1,
                internships=2,
                research_papers=2,
                coding_score=78.0
            ),
            Student(
                name="Grace Liu",
                email="grace@university.edu",
                domain_interest="Law",
                skills="Constitutional Law, International Law, Debate, Writing",
                bio="Law student focused on human rights and international policy.",
                hackathons=2,
                internships=4,
                research_papers=1,
                coding_score=82.0
            )
        ]

        db.add_all(opportunities)
        db.add_all(students)
        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - initialize database on startup."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    # Seed with initial data
    seed_database()
    yield


# Create FastAPI application
app = FastAPI(
    title="Real-Time Ivy League Opportunity Intelligence & Student Competency Network",
    description="Prototype for matching Ivy League opportunities with student competencies",
    version="0.1.0",
    lifespan=lifespan
)

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, student_id: int = None, search: str = None, domain: str = None):
    """Home page displaying opportunities and students with optional filtering."""
    db = SessionLocal()
    try:
        students = db.query(Student).all()
        selected_student = None
        
        # Base query
        query = db.query(Opportunity)
        
        # Filter by student's domain interest
        if student_id:
            selected_student = db.query(Student).filter(Student.id == student_id).first()
            if selected_student:
                query = query.filter(Opportunity.domain == selected_student.domain_interest)
        
        # Filter by domain
        if domain:
            query = query.filter(Opportunity.domain == domain)
        
        # Search by title or description
        if search:
            query = query.filter(
                (Opportunity.title.ilike(f"%{search}%")) | 
                (Opportunity.description.ilike(f"%{search}%"))
            )
        
        opportunities = query.order_by(Opportunity.posted_date.desc()).all()
        
        # Get all domains for filter dropdown
        all_domains = [d[0] for d in db.query(Opportunity.domain).distinct().all()]
        
        # Recommendations (if student selected, show matching domain opportunities not yet applied)
        recommendations = []
        if selected_student:
            applied_opp_ids = [a.opportunity_id for a in db.query(Application).filter(
                Application.student_id == selected_student.id
            ).all()]
            recommendations = db.query(Opportunity).filter(
                Opportunity.domain == selected_student.domain_interest,
                ~Opportunity.id.in_(applied_opp_ids) if applied_opp_ids else True
            ).limit(3).all()
        
        students_with_scores = [
            {"student": s, "incoscore": calculate_incoscore(s)} for s in students
        ]
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "opportunities": opportunities,
                "students": students_with_scores,
                "selected_student": selected_student,
                "all_domains": all_domains,
                "current_domain": domain,
                "search_query": search or "",
                "recommendations": recommendations
            }
        )
    finally:
        db.close()


@app.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard(request: Request):
    """Leaderboard page showing students ranked by InCoScore."""
    db = SessionLocal()
    try:
        students = db.query(Student).all()
        
        # Calculate scores and sort by descending score
        ranked_students = sorted(
            [{"student": s, "incoscore": calculate_incoscore(s)} for s in students],
            key=lambda x: x["incoscore"],
            reverse=True
        )
        
        # Add rank numbers
        for i, item in enumerate(ranked_students, start=1):
            item["rank"] = i
        
        return templates.TemplateResponse(
            "leaderboard.html",
            {
                "request": request,
                "ranked_students": ranked_students
            }
        )
    finally:
        db.close()


# ============== STUDENT PROFILE ==============

@app.get("/student/{student_id}", response_class=HTMLResponse)
async def student_profile(request: Request, student_id: int):
    """Student profile page with details and InCoScore."""
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
        
        incoscore = calculate_incoscore(student)
        applications = db.query(Application).filter(Application.student_id == student_id).all()
        
        return templates.TemplateResponse(
            "profile.html",
            {
                "request": request,
                "student": student,
                "incoscore": incoscore,
                "applications": applications
            }
        )
    finally:
        db.close()


# ============== OPPORTUNITY DETAIL ==============

@app.get("/opportunity/{opp_id}", response_class=HTMLResponse)
async def opportunity_detail(request: Request, opp_id: int):
    """Opportunity detail page."""
    db = SessionLocal()
    try:
        opportunity = db.query(Opportunity).filter(Opportunity.id == opp_id).first()
        if not opportunity:
            return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
        
        students = db.query(Student).all()
        
        return templates.TemplateResponse(
            "opportunity.html",
            {
                "request": request,
                "opportunity": opportunity,
                "students": students
            }
        )
    finally:
        db.close()


# ============== AUTO-APPLICATION SYSTEM ==============

@app.post("/apply/{opp_id}")
async def apply_to_opportunity(opp_id: int, student_id: int = Form(...)):
    """Submit application to an opportunity."""
    db = SessionLocal()
    try:
        # Check if already applied
        existing = db.query(Application).filter(
            Application.student_id == student_id,
            Application.opportunity_id == opp_id
        ).first()
        
        if not existing:
            application = Application(
                student_id=student_id,
                opportunity_id=opp_id,
                status="submitted"
            )
            db.add(application)
            db.commit()
        
        return RedirectResponse(url=f"/student/{student_id}?applied=1", status_code=303)
    finally:
        db.close()


# ============== COMMUNITY PLATFORM ==============

@app.get("/community", response_class=HTMLResponse)
async def community(request: Request):
    """Academic community - posts and discussions."""
    db = SessionLocal()
    try:
        posts = db.query(Post).order_by(Post.created_at.desc()).all()
        students = db.query(Student).all()
        
        return templates.TemplateResponse(
            "community.html",
            {
                "request": request,
                "posts": posts,
                "students": students
            }
        )
    finally:
        db.close()


@app.post("/community/post")
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    domain: str = Form(None),
    author_id: int = Form(...)
):
    """Create a new community post."""
    db = SessionLocal()
    try:
        post = Post(
            author_id=author_id,
            title=title,
            content=content,
            domain=domain if domain else None
        )
        db.add(post)
        db.commit()
        return RedirectResponse(url="/community", status_code=303)
    finally:
        db.close()


@app.post("/community/comment/{post_id}")
async def add_comment(
    post_id: int,
    content: str = Form(...),
    author_id: int = Form(...)
):
    """Add comment to a post."""
    db = SessionLocal()
    try:
        comment = Comment(
            post_id=post_id,
            author_id=author_id,
            content=content
        )
        db.add(comment)
        db.commit()
        return RedirectResponse(url="/community", status_code=303)
    finally:
        db.close()


# ============== DASHBOARD ==============

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard with analytics and stats."""
    db = SessionLocal()
    try:
        # Stats
        total_opportunities = db.query(Opportunity).count()
        total_students = db.query(Student).count()
        total_applications = db.query(Application).count()
        total_posts = db.query(Post).count()
        
        # Domain distribution
        domains = db.query(Opportunity.domain).distinct().all()
        domain_stats = []
        for (domain,) in domains:
            count = db.query(Opportunity).filter(Opportunity.domain == domain).count()
            domain_stats.append({"domain": domain, "count": count})
        
        # Recent applications
        recent_apps = db.query(Application).order_by(Application.applied_at.desc()).limit(5).all()
        
        # Top students by InCoScore
        students = db.query(Student).all()
        top_students = sorted(
            [{"student": s, "incoscore": calculate_incoscore(s)} for s in students],
            key=lambda x: x["incoscore"],
            reverse=True
        )[:3]
        
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "total_opportunities": total_opportunities,
                "total_students": total_students,
                "total_applications": total_applications,
                "total_posts": total_posts,
                "domain_stats": domain_stats,
                "recent_apps": recent_apps,
                "top_students": top_students
            }
        )
    finally:
        db.close()
