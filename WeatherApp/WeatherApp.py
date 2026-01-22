import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import threading

LIGHT_CORAL = "#f08080"
SWEET_SALMON = "#f4978e"
POWDER_BLUSH = "#f8ad9d"
PEACH_FUZZ = "#fbc4ab"
SOFT_APRICOT = "#ffdab9"
DARK_TEXT = "#2d2d2d"
LIGHT_TEXT = "#ffffff"

WEATHER_API_KEY = "40673d4f44f844669e5172055261601"

class ModernWeatherDashboard:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        
        self.temperature_unit = "Celsius"
        self.current_weather_data = None
        self.is_fetching = False
        self.animation_task = None
        self.previous_searches = []
        
        self.build_interface()
        self.setup_event_bindings()

    def setup_window(self):
        self.master.title("Modern Weather Dashboard")
        self.master.geometry("1000x900")
        self.master.configure(bg=SOFT_APRICOT)
        self.master.minsize(1000, 900)

    def build_interface(self):
        self.construct_header()
        self.construct_main_area()
        self.construct_footer()
        self.display_initial_message()

    def construct_header(self):
        header_container = tk.Frame(self.master, bg=LIGHT_CORAL, height=100)
        header_container.pack(fill=tk.X)
        header_container.pack_propagate(False)
        
        app_title = tk.Label(
            header_container,
            text="Weather Intelligence System",
            font=("Arial", 30, "bold"),
            bg=LIGHT_CORAL,
            fg=LIGHT_TEXT
        )
        app_title.pack(expand=True, pady=15)

    def construct_main_area(self):
        content_wrapper = tk.Frame(self.master, bg=SOFT_APRICOT)
        content_wrapper.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        sidebar = self.create_sidebar(content_wrapper)
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 20))

        display_area = self.create_display_area(content_wrapper)
        display_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def create_sidebar(self, parent):
        sidebar_frame = tk.Frame(parent, bg=SOFT_APRICOT, width=320)
        
        self.create_search_section(sidebar_frame)
        self.create_control_section(sidebar_frame)
        
        return sidebar_frame

    def create_search_section(self, parent):
        search_container = tk.Frame(parent, bg=POWDER_BLUSH, padx=20, pady=20)
        search_container.pack(fill=tk.X, pady=(0, 15))

        section_header = tk.Label(
            search_container,
            text="Location Search",
            font=("Arial", 14, "bold"),
            bg=POWDER_BLUSH,
            fg=DARK_TEXT
        )
        section_header.pack(anchor="w", pady=(0, 12))

        input_wrapper = tk.Frame(search_container, bg=LIGHT_TEXT, padx=3, pady=3)
        input_wrapper.pack(fill=tk.X)

        self.location_input = tk.Entry(
            input_wrapper,
            font=("Arial", 14),
            bg=LIGHT_TEXT,
            fg=DARK_TEXT,
            relief="flat",
            insertbackground=DARK_TEXT
        )
        self.location_input.pack(fill=tk.X, ipady=12, padx=4, pady=4)

        self.fetch_button = tk.Button(
            search_container,
            text="Retrieve Weather Data",
            bg=SWEET_SALMON,
            fg=LIGHT_TEXT,
            font=("Arial", 12, "bold"),
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.initiate_weather_fetch,
            activebackground=LIGHT_CORAL,
            activeforeground=LIGHT_TEXT
        )
        self.fetch_button.pack(fill=tk.X, pady=(12, 0))

        self.status_indicator = tk.Label(
            search_container,
            text="System Ready",
            font=("Arial", 9),
            bg=POWDER_BLUSH,
            fg=DARK_TEXT
        )
        self.status_indicator.pack(pady=(10, 0))

    def create_control_section(self, parent):
        control_container = tk.Frame(parent, bg=POWDER_BLUSH, padx=20, pady=20)
        control_container.pack(fill=tk.BOTH, expand=True)

        controls_header = tk.Label(
            control_container,
            text="Dashboard Controls",
            font=("Arial", 14, "bold"),
            bg=POWDER_BLUSH,
            fg=DARK_TEXT
        )
        controls_header.pack(anchor="w", pady=(0, 12))

        self.unit_toggle_button = tk.Button(
            control_container,
            text="Switch to Fahrenheit",
            bg=PEACH_FUZZ,
            fg=DARK_TEXT,
            font=("Arial", 11),
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.switch_temperature_unit,
            activebackground=POWDER_BLUSH
        )
        self.unit_toggle_button.pack(fill=tk.X, pady=(0, 10))

        self.visualization_button = tk.Button(
            control_container,
            text="Display Temperature Graph",
            bg=PEACH_FUZZ,
            fg=DARK_TEXT,
            font=("Arial", 11),
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.generate_temperature_chart,
            activebackground=POWDER_BLUSH
        )
        self.visualization_button.pack(fill=tk.X, pady=(0, 10))

        self.reload_button = tk.Button(
            control_container,
            text="Reload Current Location",
            bg=PEACH_FUZZ,
            fg=DARK_TEXT,
            font=("Arial", 11),
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.reload_current_data,
            activebackground=POWDER_BLUSH
        )
        self.reload_button.pack(fill=tk.X)

    def create_display_area(self, parent):
        display_frame = tk.Frame(parent, bg=SOFT_APRICOT)

        output_container = tk.Frame(display_frame, bg=SWEET_SALMON, padx=4, pady=4)
        output_container.pack(fill=tk.BOTH, expand=True)

        text_frame = tk.Frame(output_container, bg=LIGHT_TEXT)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.weather_display = tk.Text(
            text_frame,
            bg=LIGHT_TEXT,
            fg=DARK_TEXT,
            font=("Courier New", 11),
            relief="flat",
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        self.weather_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        display_scrollbar = tk.Scrollbar(text_frame, command=self.weather_display.yview)
        display_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.weather_display.config(yscrollcommand=display_scrollbar.set)

        self.configure_text_styles()
        
        return display_frame

    def configure_text_styles(self):
        self.weather_display.tag_config("main_temp", font=("Arial", 36, "bold"), foreground=LIGHT_CORAL)
        self.weather_display.tag_config("condition_text", font=("Arial", 16, "italic"), foreground=SWEET_SALMON)
        self.weather_display.tag_config("section_title", font=("Arial", 14, "bold"), foreground=LIGHT_CORAL)
        self.weather_display.tag_config("sub_section", font=("Arial", 12, "bold"), foreground=POWDER_BLUSH)
        self.weather_display.tag_config("info_text", font=("Courier New", 11), foreground=DARK_TEXT)
        self.weather_display.tag_config("emphasis", font=("Courier New", 11, "bold"), foreground=SWEET_SALMON)

    def construct_footer(self):
        footer_container = tk.Frame(self.master, bg=LIGHT_CORAL, height=40)
        footer_container.pack(side=tk.BOTTOM, fill=tk.X)
        footer_container.pack_propagate(False)
        
        self.footer_text = tk.Label(
            footer_container,
            text="Data Provider: WeatherAPI.com",
            font=("Arial", 10),
            bg=LIGHT_CORAL,
            fg=LIGHT_TEXT
        )
        self.footer_text.pack(expand=True)

    def setup_event_bindings(self):
        self.location_input.bind('<Return>', lambda event: self.initiate_weather_fetch())
        self.location_input.bind('<KeyRelease>', self.handle_input_change)
        
        button_configs = [
            (self.fetch_button, SWEET_SALMON, LIGHT_CORAL),
            (self.unit_toggle_button, PEACH_FUZZ, POWDER_BLUSH),
            (self.visualization_button, PEACH_FUZZ, POWDER_BLUSH),
            (self.reload_button, PEACH_FUZZ, POWDER_BLUSH)
        ]
        
        for button, default_bg, hover_bg in button_configs:
            button.bind("<Enter>", lambda e, bg=hover_bg: e.widget.config(bg=bg))
            button.bind("<Leave>", lambda e, bg=default_bg: e.widget.config(bg=bg))

    def handle_input_change(self, event):
        input_text = self.location_input.get().strip()
        if len(input_text) > 0:
            self.fetch_button.config(bg=LIGHT_CORAL, fg=LIGHT_TEXT)
        else:
            self.fetch_button.config(bg=SWEET_SALMON, fg=LIGHT_TEXT)

    def display_initial_message(self):
        self.weather_display.delete("1.0", tk.END)
        self.weather_display.insert(tk.END, "\n\n\n")
        self.weather_display.insert(tk.END, "Weather Intelligence System\n\n", "main_temp")
        self.weather_display.insert(tk.END, "Enter your location to begin\n\n", "condition_text")
        self.weather_display.insert(tk.END, "Available Features:\n", "section_title")
        self.weather_display.insert(tk.END, "  - Live weather conditions\n")
        self.weather_display.insert(tk.END, "  - Extended 5-day outlook\n")
        self.weather_display.insert(tk.END, "  - Hour-by-hour predictions\n")
        self.weather_display.insert(tk.END, "  - Air quality monitoring\n")
        self.weather_display.insert(tk.END, "  - Active weather warnings\n")
        self.weather_display.insert(tk.END, "  - Visual temperature trends\n\n")
        self.weather_display.insert(tk.END, "Hit Enter or click the button to start", "sub_section")

    def switch_temperature_unit(self):
        if self.temperature_unit == "Celsius":
            self.temperature_unit = "Fahrenheit"
            self.unit_toggle_button.config(text="Switch to Celsius")
        else:
            self.temperature_unit = "Celsius"
            self.unit_toggle_button.config(text="Switch to Fahrenheit")
        
        if self.current_weather_data:
            self.render_weather_information(self.current_weather_data)

    def modify_status(self, status_message, text_color=DARK_TEXT):
        self.status_indicator.config(text=status_message, fg=text_color)
    def start_loading_sequence(self):
        self.is_fetching = True
        self.fetch_button.config(state=tk.DISABLED, text="Fetching...")
        self.unit_toggle_button.config(state=tk.DISABLED)
        self.visualization_button.config(state=tk.DISABLED)
        self.reload_button.config(state=tk.DISABLED)
        self.run_loading_animation(0)

    def run_loading_animation(self, iteration):
        if not self.is_fetching:
            return
        
        dot_count = iteration % 4
        loading_dots = "." * dot_count + " " * (3 - dot_count)
        
        self.weather_display.delete("1.0", tk.END)
        self.weather_display.insert(tk.END, f"\n\n\n\n")
        self.weather_display.insert(tk.END, f"Loading Weather Information{loading_dots}\n\n", "main_temp")
        self.weather_display.insert(tk.END, "Retrieving latest meteorological data", "condition_text")
        self.modify_status("Fetching data from server...", SWEET_SALMON)
        
        self.animation_task = self.master.after(380, self.run_loading_animation, iteration + 1)

    def end_loading_sequence(self):
        self.is_fetching = False
        if self.animation_task:
            self.master.after_cancel(self.animation_task)
        self.fetch_button.config(state=tk.NORMAL, text="Retrieve Weather Data")
        self.unit_toggle_button.config(state=tk.NORMAL)
        self.visualization_button.config(state=tk.NORMAL)
        self.reload_button.config(state=tk.NORMAL)

    def initiate_weather_fetch(self):
        location_query = self.location_input.get().strip()
        if not location_query:
            messagebox.showwarning("Missing Input", "Please provide a location name")
            return

        fetch_thread = threading.Thread(target=self.retrieve_weather_data, args=(location_query,))
        fetch_thread.daemon = True
        fetch_thread.start()

    def reload_current_data(self):
        if self.current_weather_data:
            saved_location = self.current_weather_data['location']['name']
            self.location_input.delete(0, tk.END)
            self.location_input.insert(0, saved_location)
            self.initiate_weather_fetch()
        else:
            messagebox.showinfo("No Previous Data", "Search for a location first")

    def retrieve_weather_data(self, location):
        self.start_loading_sequence()

        try:
            api_endpoint = (
                f"https://api.weatherapi.com/v1/forecast.json"
                f"?key={WEATHER_API_KEY}&q={location}&days=5&aqi=yes&alerts=yes"
            )
            
            api_response = requests.get(api_endpoint, timeout=12)
            weather_data = api_response.json()
            
            self.master.after(0, self.end_loading_sequence)

            if "error" in weather_data:
                error_description = weather_data["error"]["message"]
                self.master.after(0, lambda: messagebox.showerror("Request Failed", error_description))
                self.master.after(0, lambda: self.modify_status(f"Error: {error_description}", LIGHT_CORAL))
                self.master.after(0, self.display_initial_message)
                return

            self.current_weather_data = weather_data
            if location not in self.previous_searches:
                self.previous_searches.append(location)
            
            self.master.after(0, lambda: self.render_weather_information(weather_data))
            self.master.after(0, lambda: self.modify_status(
                f"Successfully loaded: {weather_data['location']['name']}", 
                LIGHT_CORAL
            ))
            
            timestamp = datetime.now().strftime("%I:%M %p on %B %d, %Y")
            self.master.after(0, lambda: self.footer_text.config(
                text=f"Updated: {timestamp} | Data Provider: WeatherAPI.com"
            ))

        except requests.Timeout:
            self.master.after(0, self.end_loading_sequence)
            self.master.after(0, lambda: messagebox.showerror("Timeout Error", "The request took too long. Check your connection."))
            self.master.after(0, lambda: self.modify_status("Request timeout occurred", LIGHT_CORAL))
        except requests.ConnectionError:
            self.master.after(0, self.end_loading_sequence)
            self.master.after(0, lambda: messagebox.showerror("Network Issue", "Cannot reach weather service. Verify internet connection."))
            self.master.after(0, lambda: self.modify_status("Network error detected", LIGHT_CORAL))
        except Exception as error:
            self.master.after(0, self.end_loading_sequence)
            self.master.after(0, lambda: messagebox.showerror("Unexpected Error", f"Something went wrong:\n{str(error)}"))
            self.master.after(0, lambda: self.modify_status("System error occurred", LIGHT_CORAL))

    def render_weather_information(self, weather_data):
        self.weather_display.delete("1.0", tk.END)

        live_conditions = weather_data["current"]
        place_info = weather_data["location"]
        forecast_data = weather_data["forecast"]["forecastday"]

        is_celsius = self.temperature_unit == "Celsius"
        current_temp = live_conditions["temp_c"] if is_celsius else live_conditions["temp_f"]
        perceived_temp = live_conditions["feelslike_c"] if is_celsius else live_conditions["feelslike_f"]
        wind_velocity = live_conditions["wind_kph"] if is_celsius else live_conditions["wind_mph"]
        velocity_unit = "km/h" if is_celsius else "mph"
        degree_symbol = "°C" if is_celsius else "°F"

        self.weather_display.insert(tk.END, f"\n{current_temp:.1f}{degree_symbol}\n", "main_temp")
        self.weather_display.insert(tk.END, f"{live_conditions['condition']['text']}\n", "condition_text")
        self.weather_display.insert(tk.END, f"Perceived temperature: {perceived_temp:.1f}{degree_symbol}\n\n", "condition_text")
        
        self.weather_display.insert(tk.END, f"{place_info['name']}, {place_info['country']}\n", "section_title")
        self.weather_display.insert(tk.END, f"Current local time: {place_info['localtime']}\n")
        self.weather_display.insert(tk.END, "━" * 75 + "\n\n", "info_text")

        self.weather_display.insert(tk.END, "Live Atmospheric Conditions\n", "section_title")
        self.weather_display.insert(tk.END, f"Moisture Level   : {live_conditions['humidity']}%\n", "info_text")
        self.weather_display.insert(tk.END, f"Wind Velocity    : {wind_velocity:.1f} {velocity_unit} from {live_conditions['wind_dir']}\n", "info_text")
        self.weather_display.insert(tk.END, f"Cloud Coverage   : {live_conditions['cloud']}%\n", "info_text")
        self.weather_display.insert(tk.END, f"Visibility Range : {live_conditions['vis_km']} km\n", "info_text")
        self.weather_display.insert(tk.END, f"Barometric Press : {live_conditions['pressure_mb']} mb\n", "info_text")
        
        uv_value = live_conditions['uv']
        uv_category = self.categorize_uv_index(uv_value)
        self.weather_display.insert(tk.END, f"UV Radiation     : {uv_value} ", "info_text")
        self.weather_display.insert(tk.END, f"[{uv_category}]\n", "emphasis")
        
        if 'air_quality' in live_conditions and live_conditions['air_quality']:
            aqi_value = live_conditions['air_quality'].get('us-epa-index', 'N/A')
            aqi_category = self.interpret_aqi(aqi_value)
            self.weather_display.insert(tk.END, f"Air Quality Idx  : {aqi_value} [{aqi_category}]\n", "info_text")
        
        self.weather_display.insert(tk.END, "\n" + "━" * 75 + "\n\n", "info_text")        
        self.weather_display.insert(tk.END, "Hour-by-Hour Outlook (Next 12 Hours)\n\n", "section_title")
        present_hour = datetime.now().hour
        displayed_hours = 0
        
        for day_data in forecast_data:
            if displayed_hours >= 12:
                break
            for hour_data in day_data["hour"]:
                hour_value = int(hour_data['time'].split()[1].split(':')[0])
                if hour_value >= present_hour and displayed_hours < 12:
                    hourly_temp = hour_data["temp_c"] if is_celsius else hour_data["temp_f"]
                    rain_probability = hour_data.get('chance_of_rain', 0)
                    self.weather_display.insert(
                        tk.END,
                        f"{hour_data['time'][11:16]}  ║  {hourly_temp:5.1f}{degree_symbol}  ║  {hour_data['condition']['text']:22s}  ║  Precipitation: {rain_probability}%\n",
                        "info_text"
                    )
                    displayed_hours += 1
            present_hour = 0

        self.weather_display.insert(tk.END, "\n" + "━" * 75 + "\n\n", "info_text")

        self.weather_display.insert(tk.END, "Extended 5-Day Weather Outlook\n\n", "section_title")
        for day_data in forecast_data:
            formatted_date = datetime.strptime(day_data['date'], '%Y-%m-%d').strftime('%A, %b %d')
            high_temp = day_data["day"]["maxtemp_c"] if is_celsius else day_data["day"]["maxtemp_f"]
            low_temp = day_data["day"]["mintemp_c"] if is_celsius else day_data["day"]["mintemp_f"]
            sky_condition = day_data["day"]["condition"]["text"]
            precipitation_chance = day_data["day"].get("daily_chance_of_rain", 0)
            self.weather_display.insert(
                tk.END,
                f"{formatted_date:18}  ║  High: {high_temp:5.1f}{degree_symbol}  Low: {low_temp:5.1f}{degree_symbol}  ║  {sky_condition:22s}  ║  Rain: {precipitation_chance}%\n",
                "info_text"
            )

        if 'alerts' in weather_data and weather_data['alerts'].get('alert'):
            self.weather_display.insert(tk.END, "\n" + "━" * 75 + "\n\n", "info_text")
            self.weather_display.insert(tk.END, "Active Weather Warnings\n\n", "section_title")
            for warning in weather_data['alerts']['alert']:
                self.weather_display.insert(tk.END, f"WARNING: {warning['headline']}\n", "emphasis")
                self.weather_display.insert(tk.END, f"Details: {warning.get('desc', 'No additional information')}\n\n", "info_text")

    def categorize_uv_index(self, uv_level):
        if uv_level <= 2:
            return "Minimal"
        elif uv_level <= 5:
            return "Moderate"
        elif uv_level <= 7:
            return "High"
        elif uv_level <= 10:
            return "Very High"
        else:
            return "Extreme"

    def interpret_aqi(self, aqi_index):
        aqi_categories = {
            1: "Excellent",
            2: "Fair",
            3: "Sensitive Groups Alert",
            4: "Unhealthy",
            5: "Very Unhealthy",
            6: "Hazardous"
        }
        return aqi_categories.get(aqi_index, "Unknown")

    def generate_temperature_chart(self):
        if not self.current_weather_data:
            messagebox.showwarning("Data Required", "Please fetch weather information first")
            return

        chart_window = tk.Toplevel(self.master)
        chart_window.title(f"Temperature Analysis - {self.current_weather_data['location']['name']}")
        chart_window.geometry("950x650")
        chart_window.config(bg=SOFT_APRICOT)

        date_labels = []
        maximum_temperatures = []
        minimum_temperatures = []
        average_temperatures = []

        for day_forecast in self.current_weather_data["forecast"]["forecastday"]:
            date_parsed = datetime.strptime(day_forecast["date"], '%Y-%m-%d')
            date_labels.append(date_parsed.strftime('%m/%d'))
            
            if self.temperature_unit == "Celsius":
                maximum_temperatures.append(day_forecast["day"]["maxtemp_c"])
                minimum_temperatures.append(day_forecast["day"]["mintemp_c"])
                average_temperatures.append(day_forecast["day"]["avgtemp_c"])
            else:
                maximum_temperatures.append(day_forecast["day"]["maxtemp_f"])
                minimum_temperatures.append(day_forecast["day"]["mintemp_f"])
                average_temperatures.append(day_forecast["day"]["avgtemp_f"])

        figure, axis = plt.subplots(figsize=(9.5, 6), facecolor=SOFT_APRICOT)
        axis.set_facecolor(LIGHT_TEXT)
        
        axis.plot(date_labels, maximum_temperatures, marker="o", label="Maximum", linewidth=3.5, color=LIGHT_CORAL, markersize=9)
        axis.plot(date_labels, average_temperatures, marker="s", label="Average", linewidth=3.5, color=SWEET_SALMON, markersize=9)
        axis.plot(date_labels, minimum_temperatures, marker="^", label="Minimum", linewidth=3.5, color=POWDER_BLUSH, markersize=9)
        
        axis.fill_between(date_labels, minimum_temperatures, maximum_temperatures, alpha=0.25, color=PEACH_FUZZ)
        
        location_name = self.current_weather_data['location']['name']
        axis.set_title(f"Temperature Forecast Analysis - {location_name}", fontsize=19, fontweight='bold', color=DARK_TEXT, pad=25)
        axis.set_xlabel("Date", fontsize=14, fontweight='bold', color=DARK_TEXT)
        axis.set_ylabel(f"Temperature ({'°C' if self.temperature_unit == 'Celsius' else '°F'})", fontsize=14, fontweight='bold', color=DARK_TEXT)
        axis.legend(loc='best', fontsize=12, framealpha=0.95)
        axis.grid(True, alpha=0.35, linestyle='--', linewidth=1)
        axis.tick_params(colors=DARK_TEXT, labelsize=10)
        
        canvas_widget = FigureCanvasTkAgg(figure, chart_window)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

if __name__ == "__main__":
    application_root = tk.Tk()
    weather_dashboard = ModernWeatherDashboard(application_root)
    application_root.mainloop()