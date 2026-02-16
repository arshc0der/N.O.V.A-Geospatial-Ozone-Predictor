import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import threading
import time
import requests
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # For 3D plotting
import seaborn as sns

# ==================================================
# LIBRARY CHECK
# ==================================================
try:
    import tkintermapview
except ImportError:
    messagebox.showerror("Missing Libraries", "Please run: pip install tkintermapview requests")
    exit()

# THEME
COLOR_BG          = "#0b0f19"   # Midnight Blue (Main BG)
COLOR_SIDEBAR     = "#151b2b"   # Darker Navy (Sidebar)
COLOR_CARD        = "#1e293b"   # Card Background
COLOR_ACCENT      = "#3b82f6"   # Corporate Blue
COLOR_TEXT        = "#f8fafc"   # White text
COLOR_SUBTEXT     = "#94a3b8"   # Grey text
COLOR_DANGER      = "#ef4444"   # Red
COLOR_WARNING     = "#f59e0b"   # Orange
COLOR_SUCCESS     = "#10b981"   # Green

FONT_HERO         = ("Segoe UI", 26, "bold")
FONT_H1           = ("Segoe UI", 20, "bold")
FONT_H2           = ("Segoe UI", 16)
FONT_BODY         = ("Segoe UI", 11)
FONT_MONO         = ("Consolas", 12)

# DATA INTELLIGENCE ENGINE
class DataBrain:
    def __init__(self):
        self.df = None
        self.model = None
        self.accuracy = 0.0
        self.stats = {}

    def initialize(self):
        try:
            # Load Data
            self.df = pd.read_csv("Receptor_western_NAmerica_ozone_obs_1994_2021_from900to300.csv")
            
            # Pre-calculate stats for the Dashboard
            self.stats['total'] = len(self.df)
            self.stats['avg_ozone'] = round(self.df['Ozone_ppbv'].mean(), 2)
            self.stats['max_ozone'] = round(self.df['Ozone_ppbv'].max(), 2)
            
            # Sampling for AI Training (Speed optimization)
            df_sample = self.df.sample(frac=0.2, random_state=42)
            
            # Features & Target
            X = df_sample[['Pressure', 'Year', 'Month', 'Latitude', 'Longitude']]
            y = df_sample['Ozone_ppbv']
            
            # Train/Test Split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Model
            self.model = RandomForestRegressor(n_estimators=50, max_depth=12, n_jobs=-1)
            self.model.fit(X_train, y_train)
            self.accuracy = round(self.model.score(X_test, y_test) * 100, 2)
            
            return True
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            return False

brain = DataBrain()

# APPLICATION UI
class OzoneEnterpriseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NASA/N.O.V.A | ATMOSPHERIC INTELLIGENCE PLATFORM")
        self.root.geometry("1500x950")
        self.root.configure(bg=COLOR_BG)
        
        self.is_tracking_iss = False

        # Init Data
        if not brain.initialize():
            messagebox.showerror("System Failure", "Could not load dataset. Check CSV file.")
            root.destroy()
            return

        self.setup_layout()
        self.show_dashboard()

    def setup_layout(self):
        # --- SIDEBAR (Navigation) ---
        self.sidebar = tk.Frame(self.root, bg=COLOR_SIDEBAR, width=300)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand
        tk.Label(self.sidebar, text="FLEXPART\nENTERPRISE", bg=COLOR_SIDEBAR, fg=COLOR_ACCENT, 
                 font=("Segoe UI", 22, "bold"), pady=40).pack()

        # Menu
        self.create_nav_btn("📊  EXECUTIVE DASHBOARD", self.show_dashboard)
        self.create_nav_btn("📈  DEEP ANALYSIS", self.show_analysis)
        self.create_nav_btn("🤖  PREDICTIVE AI", self.show_prediction)
        self.create_nav_btn("🛰️  SATELLITE FEED", self.show_api_feed)
        
        # System Info
        info_box = tk.Frame(self.sidebar, bg=COLOR_BG, padx=10, pady=10)
        info_box.pack(side="bottom", fill="x", padx=20, pady=20)
        tk.Label(info_box, text="SYSTEM STATUS", bg=COLOR_BG, fg="#555", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(info_box, text="● ONLINE", bg=COLOR_BG, fg=COLOR_SUCCESS, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(info_box, text=f"AI Accuracy: {brain.accuracy}%", bg=COLOR_BG, fg=COLOR_SUBTEXT, font=FONT_BODY).pack(anchor="w")

        # --- MAIN CONTENT AREA ---
        self.main_area = tk.Frame(self.root, bg=COLOR_BG)
        self.main_area.pack(side="left", fill="both", expand=True)

    def create_nav_btn(self, text, command):
        btn = tk.Button(self.sidebar, text=text, bg=COLOR_SIDEBAR, fg=COLOR_TEXT, 
                        font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2", anchor="w", padx=30, pady=15,
                        activebackground=COLOR_ACCENT, activeforeground="white", command=command)
        btn.pack(fill="x", pady=2)

    def clear_main(self):
        self.is_tracking_iss = False
        for widget in self.main_area.winfo_children():
            widget.destroy()

    # ==================================================
    # PAGE 1: EXECUTIVE DASHBOARD (Stat Cards + Map)
    # ==================================================
    def show_dashboard(self):
        self.clear_main()
        
        # Header
        tk.Label(self.main_area, text="EXECUTIVE OVERVIEW", font=FONT_H1, bg=COLOR_BG, fg="white").pack(anchor="w", padx=30, pady=20)

        # --- STAT CARDS ROW ---
        stats_frame = tk.Frame(self.main_area, bg=COLOR_BG)
        stats_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        self.create_card(stats_frame, "AVG OZONE LEVEL", f"{brain.stats['avg_ozone']} ppbv", "Global Average", COLOR_ACCENT)
        self.create_card(stats_frame, "MAX RECORDED", f"{brain.stats['max_ozone']} ppbv", "Critical Spike", COLOR_DANGER)
        self.create_card(stats_frame, "DATA POINTS", f"{brain.stats['total']:,}", "Total Observations", COLOR_SUCCESS)
        self.create_card(stats_frame, "AI CONFIDENCE", f"{brain.accuracy}%", "R² Score", COLOR_WARNING)

        # --- MAP SECTION ---
        map_container = tk.Frame(self.main_area, bg=COLOR_CARD, bd=1, relief="solid")
        map_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(map_container, text="LIVE GEOSPATIAL DISTRIBUTION", bg=COLOR_CARD, fg="white", font=FONT_H2).pack(pady=10)
        
        self.map_widget = tkintermapview.TkinterMapView(map_container, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22) # "m" for standard map, "s" for satellite
        self.map_widget.set_position(45.0, -110.0)
        self.map_widget.set_zoom(4)
        
        # Overlay random points
        sample = brain.df.sample(n=60)
        for _, row in sample.iterrows():
            color = "red" if row['Ozone_ppbv'] > 60 else "blue"
            self.map_widget.set_marker(row['Latitude'], row['Longitude'], marker_color_circle=color, marker_color_outside=color)

    def create_card(self, parent, title, value, sub, color):
        card = tk.Frame(parent, bg=COLOR_CARD, width=300, height=120)
        card.pack(side="left", fill="both", expand=True, padx=10)
        card.pack_propagate(False)
        
        tk.Label(card, text=title, bg=COLOR_CARD, fg=COLOR_SUBTEXT, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(15, 0))
        tk.Label(card, text=value, bg=COLOR_CARD, fg=color, font=("Segoe UI", 28, "bold")).pack(anchor="w", padx=20, pady=0)
        tk.Label(card, text=sub, bg=COLOR_CARD, fg="#555", font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(0, 15))

    # ==================================================
    # PAGE 2: DEEP ANALYSIS (Interactive Graphs)
    # ==================================================
    def show_analysis(self):
        self.clear_main()
        
        # Toolbar
        toolbar = tk.Frame(self.main_area, bg=COLOR_CARD, height=60)
        toolbar.pack(fill="x", side="top", padx=30, pady=20)
        
        tk.Label(toolbar, text="VISUALIZATION ENGINE:", bg=COLOR_CARD, fg="white", font=FONT_BODY).pack(side="left", padx=20)
        
        buttons = [
            ("TRENDS", "trend"),
            ("3D PLOT", "3d"),
            ("COMPOSITION", "pie"),
            ("HEATMAP", "heatmap")
        ]
        
        for text, mode in buttons:
            tk.Button(toolbar, text=text, bg=COLOR_ACCENT, fg="white", font=("Segoe UI", 10, "bold"), bd=0, 
                      padx=15, command=lambda m=mode: self.render_graph(m)).pack(side="left", padx=5, pady=10)

        # Graph Canvas
        self.graph_frame = tk.Frame(self.main_area, bg=COLOR_BG)
        self.graph_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        self.render_graph("trend") # Default

    def render_graph(self, mode):
        for w in self.graph_frame.winfo_children(): w.destroy()
        
        fig = plt.Figure(figsize=(10, 6), dpi=100, facecolor=COLOR_BG)
        
        if mode == "trend":
            ax = fig.add_subplot(111)
            ax.set_facecolor(COLOR_CARD)
            data = brain.df.groupby('Year')['Ozone_ppbv'].mean()
            ax.plot(data.index, data.values, color=COLOR_ACCENT, marker='o', linewidth=3)
            ax.set_title("Long-Term Ozone Trend Analysis", color="white", fontsize=14)
            ax.set_xlabel("Year", color="white")
            ax.grid(color="#333", linestyle="--")
            ax.tick_params(colors='white')

        elif mode == "3d":
            ax = fig.add_subplot(111, projection='3d')
            ax.set_facecolor(COLOR_BG)
            sample = brain.df.sample(500)
            sc = ax.scatter(sample['Longitude'], sample['Latitude'], sample['Ozone_ppbv'], c=sample['Ozone_ppbv'], cmap='plasma', s=20)
            ax.set_xlabel('Longitude', color='white')
            ax.set_ylabel('Latitude', color='white')
            ax.set_zlabel('Ozone', color='white')
            ax.set_title("3D Geospatial Ozone Distribution", color="white")
            ax.tick_params(colors='white')

        elif mode == "pie":
            ax = fig.add_subplot(111)
            ax.set_facecolor(COLOR_BG)
            
            # Categorize
            def categorize(x):
                if x < 45: return "Low (<45)"
                elif x < 60: return "Medium (45-60)"
                else: return "High (>60)"
                
            counts = brain.df['Ozone_ppbv'].apply(categorize).value_counts()
            colors = [COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER]
            
            # Donut Chart
            wedges, texts, autotexts = ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=colors, pctdistance=0.85)
            
            # Draw center circle
            centre_circle = plt.Circle((0,0),0.70,fc=COLOR_BG)
            ax.add_artist(centre_circle)
            
            for t in texts: t.set_color("white")
            for t in autotexts: t.set_color("black")
            ax.set_title("Ozone Risk Composition", color="white")

        elif mode == "heatmap":
            ax = fig.add_subplot(111)
            corr = brain.df[['Pressure', 'Latitude', 'Year', 'Ozone_ppbv']].corr()
            sns.heatmap(corr, annot=True, cmap='magma', ax=ax, fmt=".2f")
            ax.tick_params(colors='white')
            ax.set_title("Correlation Matrix", color="white")

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # PAGE 3: PREDICTIVE AI (Tall Map & Animation)
    def show_prediction(self):
        self.clear_main()
        
        # Split: Inputs (Left) vs Results (Right)
        input_panel = tk.Frame(self.main_area, bg=COLOR_CARD, width=400)
        input_panel.pack(side="left", fill="y", padx=30, pady=30)
        
        result_panel = tk.Frame(self.main_area, bg=COLOR_BG)
        result_panel.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        # --- INPUTS ---
        tk.Label(input_panel, text="SIMULATION INPUTS", bg=COLOR_CARD, fg="white", font=FONT_H1).pack(pady=(20, 30))
        
        self.pred_vars = {}
        fields = [
            ("Year", "2025"),
            ("Month", "7"),
            ("Pressure (hPa)", "400"),
            ("Latitude", "49.0"),
            ("Longitude", "-123.0")
        ]
        
        for lbl, default in fields:
            f = tk.Frame(input_panel, bg=COLOR_CARD)
            f.pack(fill="x", pady=10, padx=20)
            tk.Label(f, text=lbl, bg=COLOR_CARD, fg=COLOR_SUBTEXT, width=15, anchor="w", font=FONT_BODY).pack(side="left")
            e = tk.Entry(f, bg="#0f172a", fg="white", font=FONT_BODY, relief="flat", insertbackground="white")
            e.insert(0, default)
            e.pack(side="right", fill="x", expand=True)
            self.pred_vars[lbl] = e
            
        tk.Button(input_panel, text="🚀  RUN SIMULATION", bg=COLOR_ACCENT, fg="white", font=("Segoe UI", 12, "bold"),
                  command=lambda: self.run_simulation(result_panel), pady=12, bd=0, cursor="hand2").pack(fill="x", padx=20, pady=40)

        # --- INITIAL RESULT STATE ---
        tk.Label(result_panel, text="Waiting for simulation parameters...", fg=COLOR_SUBTEXT, bg=COLOR_BG, font=FONT_H2).place(relx=0.5, rely=0.5, anchor="center")

    def run_simulation(self, parent):
        # 1. Validation & Data Prep
        try:
            inputs = {k: float(v.get()) for k, v in self.pred_vars.items()}
        except ValueError:
            messagebox.showerror("Input Error", "Please use numeric values only.")
            return
            
        # Map "Pressure (hPa)" -> "Pressure" for model
        model_input = pd.DataFrame([{
            'Pressure': inputs['Pressure (hPa)'],
            'Year': inputs['Year'],
            'Month': inputs['Month'],
            'Latitude': inputs['Latitude'],
            'Longitude': inputs['Longitude']
        }])
        
        # Predict
        prediction = brain.model.predict(model_input)[0]
        
        # 2. Build Result UI
        for w in parent.winfo_children(): w.destroy()
        
        # Top: TALL Map (Increased height per request)
        map_frame = tk.Frame(parent, height=500, bg="black") # Height 400 -> 500
        map_frame.pack(fill="x", pady=(0, 20))
        
        res_map = tkintermapview.TkinterMapView(map_frame, height=500, corner_radius=15)
        res_map.pack(fill="both")
        res_map.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        res_map.set_position(inputs['Latitude'], inputs['Longitude'])
        res_map.set_zoom(8)
        res_map.set_marker(inputs['Latitude'], inputs['Longitude'], text="TARGET ZONE")

        # Bottom: Animation & Stats
        stats_frame = tk.Frame(parent, bg=COLOR_BG)
        stats_frame.pack(fill="both", expand=True)
        
        # Animated Number
        self.lbl_pred_val = tk.Label(stats_frame, text="0.00", font=("Consolas", 48, "bold"), bg=COLOR_BG, fg="white")
        self.lbl_pred_val.pack()
        tk.Label(stats_frame, text="PREDICTED OZONE (ppbv)", fg=COLOR_SUBTEXT, bg=COLOR_BG, font=FONT_BODY).pack()
        
        # Risk Bar (Progress Bar simulation)
        self.risk_bar_frame = tk.Frame(stats_frame, bg="#333", height=20, width=400)
        self.risk_bar_frame.pack(pady=20)
        self.risk_fill = tk.Frame(self.risk_bar_frame, bg=COLOR_SUCCESS, height=20, width=0)
        self.risk_fill.place(x=0, y=0)

        # Trigger Animation
        self.animate_prediction(0, prediction)

    def animate_prediction(self, current, target):
        if current < target:
            new_val = current + (target / 30)
            
            # Color & Risk Bar Logic
            pct = min(new_val / 100, 1.0) # Assume 100 is max danger for visual
            bar_width = int(400 * pct)
            
            if new_val < 50: color = COLOR_SUCCESS
            elif new_val < 70: color = COLOR_WARNING
            else: color = COLOR_DANGER
            
            self.lbl_pred_val.config(text=f"{new_val:.2f}", fg=color)
            self.risk_fill.config(bg=color, width=bar_width)
            
            self.root.after(20, lambda: self.animate_prediction(new_val, target))
        else:
            self.lbl_pred_val.config(text=f"{target:.2f}")

    # PAGE 4: SATELLITE FEED (Robust Threading)
    def show_api_feed(self):
        self.clear_main()
        self.is_tracking_iss = True
        
        tk.Label(self.main_area, text="LIVE ORBITAL TRACKING", font=FONT_H1, bg=COLOR_BG, fg="white").pack(pady=20)
        
        # Status Box
        status_box = tk.Frame(self.main_area, bg=COLOR_CARD, padx=20, pady=20)
        status_box.pack(pady=10)
        self.lbl_api_status = tk.Label(status_box, text="ACQUIRING SIGNAL...", font=FONT_H2, bg=COLOR_CARD, fg="white")
        self.lbl_api_status.pack()
        tk.Label(status_box, text="Source: api.open-notify.org", fg=COLOR_SUBTEXT, bg=COLOR_CARD).pack()
        
        # Map
        feed_frame = tk.Frame(self.main_area, bg="black", height=500)
        feed_frame.pack(fill="x", padx=50, pady=20)
        
        self.iss_map = tkintermapview.TkinterMapView(feed_frame, height=500, corner_radius=15)
        self.iss_map.pack(fill="both")
        self.iss_map.set_zoom(2)
        
        threading.Thread(target=self.track_iss, daemon=True).start()

    def track_iss(self):
        while self.is_tracking_iss:
            try:
                r = requests.get("http://api.open-notify.org/iss-now.json", timeout=3)
                data = r.json()
                lat = float(data['iss_position']['latitude'])
                lon = float(data['iss_position']['longitude'])
                
                if not self.is_tracking_iss: break
                
                try:
                    self.lbl_api_status.config(text=f"ISS POSITION: {lat}, {lon}")
                    if self.iss_map.winfo_exists():
                        self.iss_map.set_position(lat, lon)
                        self.iss_map.set_marker(lat, lon, text="ISS LIVE", marker_color_circle="blue")
                except: break
            except: pass
            time.sleep(3)

# SYSTEM BOOT
if __name__ == "__main__":
    root = tk.Tk()
    app = OzoneEnterpriseApp(root)
    root.mainloop()