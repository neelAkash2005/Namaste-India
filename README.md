# 🌏 Namaste India - Tourism Website# 🌏 Namaste India



**Discover. Explore. Experience India!**![Website](https://img.shields.io/badge/Website-Tourism-blue) 

![HTML5](https://img.shields.io/badge/HTML5-orange) 

A modern tourism website for exploring India's vibrant cities, planning trips, and getting personalized travel recommendations.![CSS3](https://img.shields.io/badge/CSS3-blueviolet) 

![JavaScript](https://img.shields.io/badge/JS-yellow) 

---



## ✨ Features**_Discover. Explore. Experience India!_**  



- 🏙️ **City Explorer** - Detailed information on India's most popular tourist destinationsNamaste India is a **modern, user-friendly tourism website** that lets users explore India’s vibrant cities, plan trips, and enjoy a smooth booking experience—all in one place! ✨  

- 🎯 **Smart Recommender** - Get city recommendations based on month and trip duration

- 🛎️ **Booking Portal** - Interactive booking interface for hotels and trips---

- 📱 **Responsive Design** - Works perfectly on all devices

- 🔐 **User Authentication** - Secure login and signup system## 🌟 Features

- 🎨 **Modern UI** - Clean, intuitive interface with smooth animations

| Feature | Description | Icon |

---|---------|-------------|------|

| City Recommender | Curated recommendations for iconic cities in India | 🏙️ |

## 🚀 Getting Started| Booking Simulation | Interactive booking portal for hotels & trips | 🛎️ |

| Responsive Design | Works perfectly on desktop, tablet, and mobile | 📱 |

### Prerequisites| User-Friendly Navigation | Smooth login/signup and clear menus | 🧭 |

- Python 3.8+| Know More Sections | Click to explore city details and attractions | 🔍 |

- pip| Modern UI/UX | Minimalistic, clean, and visually appealing design | 🎨 |



### Installation---



1. **Clone the repository**## 🖼 Project Preview

```bash

git clone <repository-url>

cd Namaste-India*Simple, clean interface for an intuitive experience!*  

```

---

2. **Install dependencies**

```bash## 🛠 Technologies Used

pip install -r requirements.txt

```**Frontend:**  

- HTML5 – Semantic page structure  

3. **Prepare the data** (first time only)- CSS3 – Styling, animations, and responsive layouts  

```bash- JavaScript – Interactivity, dynamic elements, and login simulation  

python prepare_data.py

```**Extras:**  

- Local storage/session handling for **login simulation**  

4. **Run the application**- Hover effects and smooth animations for better **UI/UX**  

```bash

python app.py---

```

## 🚀 Getting Started

5. **Open your browser**

```Follow these **3 simple steps** to run the project locally:  

http://localhost:5000

```<div align="center">



---| Step | Action | Icon |

|------|--------|------|

## 📖 Using the Recommendation System| 1 | Clone the repository | 📥 |

| 2 | Open `index.html` in your browser | 🌐 |

1. Scroll to the **City Recommender** section on the homepage| 3 | Explore cities & demo bookings | 🧭 |

2. Enter a **month** (e.g., October, December, June)

3. Optionally enter **trip duration** in days</div>

4. Click **Recommend** to see personalized suggestions

5. Results are sorted by rating - highest rated cities first**Command to clone:**  

6. Click any city card to explore more details```bash

git clone <repository-url>

**Example queries:**

- "October" - Shows all cities great for October---

- "December" + "3 days" - Shows cities perfect for a 3-day December trip



---


## 📁 Project Structure

```
Namaste-India/
├── app.py                  # Flask application
├── prepare_data.py         # Data preprocessing script
├── City.csv                # City information (96 cities)
├── Places.csv              # Tourist attractions (2,989 places)
├── merged_df.pkl           # Processed data for recommendations
├── requirements.txt        # Python dependencies
└── static/
    ├── index.html         # Main homepage
    ├── login.html         # Login page
    ├── signup.html        # Signup page
    ├── styles.css         # Global styles
    └── [city pages]       # Individual city pages
```

---

## 🛠️ Technologies

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive design with CSS Grid & Flexbox
- Async API calls with Fetch API

**Backend:**
- Python 3.8+
- Flask - Web framework
- Pandas - Data processing
- NumPy - Numerical computations

**Data:**
- 96 cities across India
- 2,989 tourist attractions
- Real ratings and seasonal information

---

## 🎨 Features in Detail

### Smart City Recommender
The recommendation engine uses real data to suggest cities based on:
- **Best time to visit** - Matches your chosen month with ideal seasons
- **Trip duration** - Finds cities that fit your available days
- **Ratings** - Prioritizes highly-rated destinations
- **Flexibility** - Works with partial inputs (month only or month + duration)

### City Pages
Each city has a dedicated page with:
- Popular attractions
- Best time to visit
- Ideal trip duration
- Ratings and reviews
- Beautiful imagery

### Booking System
Simulated booking interface for:
- Hotels and accommodations
- Tour packages
- Transportation

---

## 🔧 Configuration

To update the dataset:
1. Edit `City.csv` or `Places.csv`
2. Run `python prepare_data.py`
3. Restart the Flask application

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- Tourism data compiled from various travel guides
- Built with Flask, Pandas, and modern web technologies
- Inspired by the incredible diversity of India

---

**Made with ❤️ for travelers exploring India** 🇮🇳
