# Phase 7 Frontend UI - Quick Start Guide

**Status:** ✅ COMPLETE & READY TO USE  
**Last Updated:** October 27, 2025

---

## 🎯 Quick Links

### Email Management (Admin Only)
**URL:** `http://localhost:8081/email-management.html`

**Requirements:** 
- Must be logged in as admin user
- Backend must be running on port 8000
- Frontend must be running on port 8081

**What You Can Do:**
1. ✅ View and edit email templates
2. ✅ Send emails to users (all, specific, or manual)
3. ✅ Monitor email queue in real-time
4. ✅ View email delivery history
5. ✅ Retry failed emails
6. ✅ Cancel pending emails

**Key Features:**
- 4-tab interface: Templates | Send | Queue | History
- Auto-refresh queue every 30 seconds
- Email preview before sending
- Template variables support: {user_name}, {job_title}, etc.
- Search and filter capabilities
- Responsive design for mobile

---

### Resume Upload & Management (All Users)
**URL:** `http://localhost:8081/resume-management.html`

**Requirements:**
- Must be logged in as any user
- Backend must be running on port 8000
- Frontend must be running on port 8081

**What You Can Do:**
1. ✅ Upload resume via drag-and-drop
2. ✅ Automatic resume data parsing
3. ✅ Edit extracted information (name, email, skills, experience, education)
4. ✅ Add/remove skills manually
5. ✅ Download original resume file
6. ✅ Delete and re-upload resume
7. ✅ View parsing confidence score

**Key Features:**
- Drag-and-drop upload with progress bar
- Automatic parsing of personal info, skills, experience, education
- Editable parsed data
- File validation (PDF, DOC, DOCX, max 5MB)
- Download and preview options
- Responsive design for mobile

---

## 🚀 Getting Started

### Prerequisites
Make sure both servers are running:

```bash
# Terminal 1 - Backend
cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service
source venv_py311/bin/activate
uvicorn src.main:app --reload

# Terminal 2 - Frontend
cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/frontend/meta-ui/public
python3 -m http.server 8081
```

### Test Credentials
```
Email: alice5678@example.com
Password: SecurePass@123
Role: User (can upload resume)
```

For admin features, create an admin account or modify user in database.

---

## 📋 Email Management Workflow

### Sending an Email

1. Navigate to `http://localhost:8081/email-management.html`
2. Click on **"Send Email"** tab
3. Select recipient type:
   - **All Users** - sends to everyone
   - **Specific User** - enter email address
   - **Manual Entry** - comma-separated emails
4. Select an email template (or type custom)
5. Edit subject and body as needed
6. Click **"Preview"** to see how it looks
7. Click **"Send Email"** to queue
8. Check **"Email Queue"** tab to monitor delivery

### Managing Templates

1. Go to **"Email Templates"** tab
2. View all templates in table
3. Click **"Edit"** to modify subject/body
4. Click **"Delete"** to remove template
5. Click **"Create Template"** to add new template

### Monitoring Queue

1. Go to **"Email Queue"** tab
2. See statistics:
   - Total pending emails
   - Failed emails
   - Sent today
   - Success rate
3. Click **"Refresh Now"** to update immediately
4. Queue auto-refreshes every 30 seconds
5. Retry failed emails with **"Retry"** button
6. Cancel pending with **"Cancel"** button

### View History

1. Go to **"Email History"** tab
2. Search by recipient email
3. Filter by date or status
4. Click **"View"** to see email details
5. Export to CSV with **"Export CSV"** button

---

## 📸 Resume Upload Workflow

### Uploading Resume

1. Navigate to `http://localhost:8081/resume-management.html`
2. Drag and drop resume file on drop zone
   - OR click zone to browse files
3. Supported formats: PDF, DOC, DOCX
4. Max file size: 5MB
5. Watch progress bar during upload
6. System automatically parses resume

### Reviewing Parsed Data

After upload, review extracted information:
- **Personal Info:** Name, email, phone
- **Skills:** Auto-extracted skills (edit as needed)
- **Work Experience:** Jobs and dates
- **Education:** Schools and degrees
- **Confidence Score:** Parsing accuracy percentage

### Editing Parsed Data

1. Review auto-extracted data
2. Edit fields directly in the display
3. Add skills using skill input
   - Type skill name and press Enter
   - Click X to remove skill
4. Click **"Save Resume Data"** when done

### Managing Resume

1. View resume file details at top
2. **Preview** - View original file in browser
3. **Download** - Save file to computer
4. **Delete** - Remove resume (click to upload new)
5. **Upload Different** - Replace with new resume

---

## 🔧 API Integration Details

### Email API Endpoints Used
```
GET  /api/email/templates           → Get all templates
POST /api/email/send                → Send email
GET  /api/email/queue               → Get pending emails
GET  /api/admin/email/statistics    → Get stats
POST /api/email/retry/{id}          → Retry failed
POST /api/email/cancel/{id}         → Cancel pending
GET  /api/email/history             → Get history
```

### File Upload API Endpoints Used
```
POST /api/files/upload              → Upload file
GET  /api/files/{file_id}           → Get file info
GET  /api/files/download/{file_id}  → Download file
DELETE /api/files/{file_id}         → Delete file
POST /api/resumes/parse             → Parse resume
GET  /api/resumes/my-resume         → Get my resume
```

---

## 🎨 UI Features & Design

### Color Scheme
- **Primary Purple:** #7C5BA6 (buttons, headers)
- **Light Purple:** #E8DFF5 (backgrounds)
- **Success Green:** #5BA85C (success badges)
- **Error Red:** #D9534F (error badges)

### Interactive Elements
- Smooth hover effects on buttons
- Loading spinners during operations
- Success/error toast messages
- Real-time data updates
- Responsive grid layouts
- Mobile-friendly design

### User Feedback
- Clear success messages ("Email sent successfully!")
- Helpful error messages with reasons
- Progress indicators for uploads
- Loading states for async operations
- Empty states with guidance

---

## 🧪 Testing the Features

### Email Testing Checklist
- [ ] Can load and view email templates
- [ ] Can edit template subject and body
- [ ] Can send email to all users
- [ ] Can send email to specific user
- [ ] Can send email to multiple manual emails
- [ ] Email appears in queue after sending
- [ ] Queue auto-refreshes every 30 seconds
- [ ] Can retry failed emails
- [ ] Can cancel pending emails
- [ ] Email history shows sent emails
- [ ] Can search and filter email history
- [ ] All alerts appear correctly
- [ ] Responsive design works on mobile

### Resume Testing Checklist
- [ ] Can drag and drop resume file
- [ ] Can click to browse and select file
- [ ] File validation works (type, size)
- [ ] Progress bar shows during upload
- [ ] Resume data automatically parsed
- [ ] Parsed info displays correctly
- [ ] Can edit parsed data fields
- [ ] Can add and remove skills
- [ ] Can preview resume file
- [ ] Can download resume file
- [ ] Can delete resume
- [ ] Can upload new resume after delete
- [ ] Confidence score displays
- [ ] Responsive design works on mobile

---

## 🐛 Troubleshooting

### Email Management Not Loading
**Problem:** Page shows "Loading..." or blank  
**Solution:** 
1. Check backend is running on port 8000
2. Check you're logged in as admin user
3. Check browser console for errors (F12)
4. Refresh page (Cmd+R or Ctrl+R)

### Can't Send Email
**Problem:** "Failed to send email" message  
**Solution:**
1. Verify recipient email is valid
2. Check network in browser DevTools
3. Verify backend API is responding (check /docs)
4. Try with "Send to All Users" option

### Email Queue Not Updating
**Problem:** Queue shows old data  
**Solution:**
1. Click "Refresh Now" button
2. Check auto-refresh is working (should refresh every 30 seconds)
3. Refresh page if needed
4. Check backend is still running

### Resume Upload Fails
**Problem:** Upload error message appears  
**Solution:**
1. Check file format is PDF, DOC, or DOCX
2. Check file size is under 5MB
3. Check backend is running
4. Try with different file
5. Check network in browser DevTools

### Parsed Data Not Showing
**Problem:** Resume uploaded but no data displayed  
**Solution:**
1. Wait a moment (parsing takes time)
2. Refresh page
3. Check browser console for errors
4. Try uploading different resume
5. Check backend parsing endpoint

---

## 📱 Mobile Access

Both features are fully responsive:

### Email Management on Mobile
- Tabs remain accessible with horizontal scroll
- Tables stack vertically for small screens
- Buttons scale to touch-friendly size
- Form inputs expand for easier data entry

### Resume Upload on Mobile
- Drop zone becomes large touch target
- File input works with mobile file picker
- Parsed data sections stack vertically
- Buttons are touch-friendly
- All controls accessible without horizontal scroll

---

## 🔐 Security Notes

- **Authentication:** All features require valid JWT token
- **Authorization:** Email management requires admin role
- **Data:** No sensitive data stored in browser (localStorage only stores token)
- **File Upload:** Backend validates file type and size
- **API:** All requests include Authorization header with JWT token

---

## ⚡ Performance Tips

1. **Email Queue:** Auto-refreshes every 30 seconds (normal)
2. **File Upload:** Progress bar provides feedback during upload
3. **Parsing:** Resume parsing takes 2-5 seconds (normal)
4. **Table Loading:** History loads on demand
5. **Memory:** Page handles large email histories smoothly

---

## 📞 Support

### Common Questions

**Q: Can I use both features at the same time?**  
A: Yes! Open both pages in different browser tabs.

**Q: How long does resume parsing take?**  
A: Typically 2-5 seconds depending on resume size.

**Q: Can I send emails to external addresses?**  
A: Yes, use "Manual Entry" mode with any email address.

**Q: What if parsing fails on my resume?**  
A: You can manually edit the extracted data or upload a cleaner resume.

**Q: Are sent emails actually delivered?**  
A: Backend has SMTP integration configured (check backend settings for email service).

---

## 🚀 Next Steps

1. **Test Email Features**
   - Send test emails
   - Monitor queue
   - Check history

2. **Test Resume Upload**
   - Upload sample resume
   - Review parsed data
   - Edit and save

3. **Integration Testing**
   - Use resume when applying for jobs
   - Receive confirmation emails
   - End-to-end workflow

4. **Admin Management**
   - View all user resumes
   - Monitor email statistics
   - Manage templates

---

## 📚 Documentation References

- **API Testing:** `PHASE_7_API_TESTING_GUIDE.md`
- **Implementation Details:** `PHASE_7_FRONTEND_UI_IMPLEMENTATION.md`
- **Backend Architecture:** `architecture_and_roadmap.md`
- **Swagger UI:** http://localhost:8000/docs

---

**Ready to use! Navigate to the links above and start managing emails and resumes. 🎉**

For issues or improvements, refer to the full documentation or check the browser console for detailed error messages.
