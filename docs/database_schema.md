# Database Schema Design - JAPS

## Overview
This document defines the complete database schema for all portals in the Job Application Portal System (JAPS). Each portal maintains its own SQLite database with specific tables and relationships.

---

## 1. JAPS Main Database (`japs_main.db`)

### Tables

#### companies
```sql
CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    api_endpoint VARCHAR(255) NOT NULL,
    portal_url VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### aggregated_jobs
```sql
CREATE TABLE aggregated_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    external_job_id VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    location VARCHAR(100),
    salary_range VARCHAR(50),
    job_type VARCHAR(50),
    experience_level VARCHAR(50),
    description TEXT,
    requirements TEXT,
    last_synced TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(company_id, external_job_id)
);
```

#### sync_logs
```sql
CREATE TABLE sync_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    sync_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    jobs_fetched INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'success',
    error_message TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);
```

---

## 2. Meta Portal Database (`meta.db`)

### Tables

#### users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

#### jobs
```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    department VARCHAR(100),
    location VARCHAR(100),
    job_type VARCHAR(50) DEFAULT 'Full-time',
    experience_level VARCHAR(50),
    salary_min INTEGER,
    salary_max INTEGER,
    description TEXT NOT NULL,
    requirements TEXT,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

#### applications
```sql
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    cover_letter TEXT,
    additional_info TEXT,
    status VARCHAR(50) DEFAULT 'submitted',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    UNIQUE(user_id, job_id)
);
```

#### user_sessions
```sql
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 3. Amazon Portal Database (`amazon.db`)

### Tables

#### users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    linkedin_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

#### jobs
```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    team VARCHAR(100),
    location VARCHAR(100),
    job_type VARCHAR(50) DEFAULT 'Full-time',
    experience_level VARCHAR(50),
    salary_min INTEGER,
    salary_max INTEGER,
    description TEXT NOT NULL,
    requirements TEXT,
    qualifications TEXT,
    benefits TEXT,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    application_deadline TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

#### applications
```sql
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    cover_letter TEXT,
    why_amazon TEXT,
    availability_date DATE,
    willing_to_relocate BOOLEAN DEFAULT 0,
    salary_expectation INTEGER,
    status VARCHAR(50) DEFAULT 'submitted',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    UNIQUE(user_id, job_id)
);
```

#### work_experience
```sql
CREATE TABLE work_experience (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    company_name VARCHAR(100) NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    description TEXT,
    is_current BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### education
```sql
CREATE TABLE education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    school_name VARCHAR(200) NOT NULL,
    degree VARCHAR(100) NOT NULL,
    field_of_study VARCHAR(100),
    graduation_year INTEGER,
    gpa DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 4. Google Portal Database (`google.db`)

### Tables

#### users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    github_url VARCHAR(255),
    portfolio_url VARCHAR(255),
    preferred_pronouns VARCHAR(50),
    diversity_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

#### jobs
```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    team VARCHAR(100),
    location VARCHAR(100),
    job_type VARCHAR(50) DEFAULT 'Full-time',
    experience_level VARCHAR(50),
    salary_min INTEGER,
    salary_max INTEGER,
    description TEXT NOT NULL,
    requirements TEXT,
    preferred_qualifications TEXT,
    responsibilities TEXT,
    minimum_qualifications TEXT,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

#### applications
```sql
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    cover_letter TEXT,
    why_google TEXT,
    relevant_experience TEXT,
    coding_challenge_completed BOOLEAN DEFAULT 0,
    status VARCHAR(50) DEFAULT 'submitted',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    UNIQUE(user_id, job_id)
);
```

#### resumes
```sql
CREATE TABLE resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    file_path VARCHAR(500),
    file_size INTEGER,
    mime_type VARCHAR(100),
    parsed_content TEXT,
    skills_extracted TEXT,
    experience_years INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### skills
```sql
CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    proficiency_level VARCHAR(50), -- Beginner, Intermediate, Advanced, Expert
    years_experience INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, skill_name)
);
```

---

## 5. Data Relationships & Constraints

### Key Relationships:
1. **Portal Isolation**: No foreign keys between different portal databases
2. **User-Application**: One-to-many (user can apply to multiple jobs)
3. **Job-Application**: One-to-many (job can have multiple applications)
4. **Unique Constraints**: User can only apply once per job in each portal

### Data Validation Rules:
1. **Email Format**: Valid email addresses required
2. **Password Security**: Minimum 8 characters, hashed storage
3. **Date Validation**: Future dates for application deadlines
4. **File Upload**: Resume file size limits (5MB max)
5. **Status Values**: Predefined status values for applications

---

## 6. Indexing Strategy

### Performance Indexes:
```sql
-- For frequent lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_applications_user_id ON applications(user_id);
CREATE INDEX idx_applications_job_id ON applications(job_id);
CREATE INDEX idx_jobs_active ON jobs(is_active);
CREATE INDEX idx_applications_status ON applications(status);

-- For aggregated jobs sync
CREATE INDEX idx_aggregated_jobs_company ON aggregated_jobs(company_id);
CREATE INDEX idx_aggregated_jobs_sync ON aggregated_jobs(last_synced);
```

---

## 7. Sample Data Requirements

### Test Data Strategy:
1. **Pre-populate** each database with sample jobs (5-10 per portal)
2. **Test users** for automation testing
3. **Varied application statuses** for testing workflows
4. **Different user profiles** to test form validations

### Automation Testing Hooks:
1. **Database Reset Scripts**: Clear and repopulate test data
2. **Data Validation Queries**: Verify test results
3. **Sample File Uploads**: Test resume processing (Google portal)

---

## 8. Migration & Maintenance

### Database Versioning:
1. **Schema Version Tracking**: Version table in each database
2. **Migration Scripts**: SQL scripts for schema updates
3. **Backup Strategy**: Regular SQLite database backups
4. **Data Cleanup**: Periodic cleanup of old sessions/logs

This schema supports the full automation testing lifecycle with realistic data relationships and enterprise-grade structure.
