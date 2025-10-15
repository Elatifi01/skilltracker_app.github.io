# 📚 SkillTracker - My Learning Journey App

Hey there! 👋 This is my first Django web application that I built during my coding bootcamp. It's basically a personal learning tracker that helps me (and hopefully you!) keep track of all the programming skills I'm learning.

## 🤔 Why I Built This

I was struggling to keep track of what I was learning, how much time I was spending on different topics, and what goals I wanted to achieve. I had notes everywhere - my phone, sticky notes, random text files - it was a mess! So I thought, "Why not build something to solve this problem?" And here we are! 🎉

## ✨ What This App Can Do

### 👤 User Stuff (The Basics)
- You can sign up and log in (pretty standard stuff!)
- Upload a profile picture because why not look good while learning? 📸
- Set your skill level (beginner, intermediate, advanced )
- Write a little bio about yourself

### 🧠 Learning Features (The Fun Part!)
- **Skills**: I can add all the different things I'm learning like Python, JavaScript, React, etc.
- **Progress Tracking**: Every day I study, I log how many hours I spent and what I worked on
- **Goals**: I set myself goals like "Finish the Django tutorial by next Friday" (sometimes I actually meet them! 😅)
- **Resources**: All my learning materials in one place - YouTube videos, articles, online courses, you name it

### � Dashboard (My Favorite Part!)
- See how many total hours I've logged (it's motivating to see the number grow!)
- Check how many goals I've actually completed vs how many I'm still working on
- Quick view of what I've been working on recently
- Reminders about upcoming deadlines (because I definitely need those!)
- Charts that show my progress over time - it actually looks pretty cool! 📈

### �️ Admin Panel (For When I Feel Powerful)
- There's this cool admin interface where I can see everything from a bird's eye view
- I can manage all the data, search through stuff, and feel like a real developer! 💪



## 🚀 Want to Try It Out?

### What You'll Need
- Python (I'm using 3.8+, but newer versions should work fine)
- Some basic command line knowledge 

### Getting It Running

1. **Get the code**
   ```bash
   # If you're cloning from somewhere, otherwise just navigate to the folder
   cd skilltracker_app
   ```

2. **Install the required packages**
   ```bash
   pip install django pillow chart.js
   # Pillow is for handling profile pictures, Chart.js for those cool graphs!
   ```

3. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   # This creates all the database tables - Django magic! ✨
   ```

4. **Create your admin account**
   ```bash
   python manage.py createsuperuser
   # Pick a username and password you'll remember!
   ```

5. **Fire it up!**
   ```bash
   python manage.py runserver
   # Your app will be running at http://127.0.0.1:8000/
   ```

6. **Check it out**
   - Main app: http://127.0.0.1:8000/ (this is where the magic happens!)
   - Admin area: http://127.0.0.1:8000/admin/ (feel like a boss here!)

## 📱 How to Use It 

### If you're just learning like me:
1. **Sign up** - create your account (use a real email if you want!)
2. **Dashboard** - this is your home base, shows all your stats
3. **Skills** - add the programming languages/frameworks you're learning
4. **Log Progress** - every time you study, log it here (be honest about your hours!)
5. **Set Goals** - give yourself deadlines (they help, trust me!)
6. **Save Resources** - bookmark all those helpful tutorials and articles
7. **Update Profile** - make it yours with a profile pic and bio

### If you're helping out or teaching:
1. Use the `/admin/` panel to see everything
2. You can help manage skills, check student progress, etc.
3. The search and filter tools are pretty handy!

## 🗺️ How Everything Connects

Here are the main pages and what they do:

- `/` - Your dashboard (home sweet home!)
- `/accounts/login/` - Where you sign in
- `/accounts/register/` - Where new people join
- `/accounts/profile/` - Your personal space
- `/skills/` - All the skills you can learn
- `/progress/` - Where you log your daily grind
- `/goals/` - Your learning targets
- `/resources/` - Your bookmarked learning materials
- `/admin/` - The control center (admin only!)

##  How the Data Fits Together

I had to learn about database relationships for this project. Here's the simple version:

```
You (User)
├── Your Progress Entries (what you studied each day)
├── Your Goals (what you want to achieve)
└── Your Learning Resources (your saved materials)

Skills (Programming languages, frameworks, etc.)
├── Connected to Progress Entries (what skill you practiced)
├── Connected to Goals (what skill you want to improve)
└── Connected to Resources (what skill the resource teaches)
```

Basically, everything revolves around you and the skills you're learning!

## 📂 Project Organization

```
skilltracker_app/
├── accounts/          # All the user login/register stuff
├── tracker/           # The main app with skills, progress, goals
├── templates/         # All the HTML files
├── media/            # Where profile pictures get saved
├── skilltracker/     # Django configuration files
└── manage.py         # The magic Django command center
```

##  What I Learned Building This

- How to connect models with relationships 
- Form validation is important (learned this the hard way!)
- Users should only see their own data (privacy matters!)
- Dates and times are more complicated than I thought
- Django admin is incredibly powerful and saves a lot of time

## 🐛 Known Issues (I'm Working On These!)

- Sometimes the charts take a second to load (learning about JavaScript timing)
- Profile picture upload could be more user-friendly
- Mobile view could use some work (responsive design is tricky!)
- Need better error messages for beginners

## � What's Next?

Ideas I'm excited to add when I get better at coding:

- Progress visualization with more detailed charts and graphs
- A system that recommends what to learn next
- Learning streaks and achievement badges (gamification!)
- Maybe a way to share progress with friends
- Export your progress to PDF or something
- A mobile app version (one day!)
- Connect with online learning platforms

## 🙏 Special Thanks

- Alx who helped me understand Django
- Stack Overflow for answering my million questions
- The Django documentation (confusing at first, but super helpful!)
- Coffee ☕ for keeping me awake during late coding sessions

## 📝 A Note About This Project

This is my learning project, built while I'm still figuring out web development. The code might not be perfect, but I'm proud of what I've built so far! If you're also learning, don't be afraid to start building something - you'll learn way more by doing than just watching tutorials.

---

**Keep learning, keep coding! 🎓💻**

*P.S. - If you find any bugs, please be gentle... ! 😅*

## Created by : El Atifi Haitam 
## reason : Alx final Project 