import ephem
import datetime
import matplotlib.pyplot as plt
from PIL import Image

def generate_natal_chart(birth_date, latitude, longitude):
    # Set up the birth date and time
    birth_date = birth_date.strftime('%Y/%m/%d %H:%M:%S')

    # Set up the observer with the birth location
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)

    # Create a chart figure and axes
    fig, ax = plt.subplots(6, 6)
    ax.set_aspect('equal')

    # Define the celestial objects for the natal chart
    objects = [
        ('Sun', ephem.Sun()),
        ('Moon', ephem.Moon()),
        ('Mercury', ephem.Mercury()),
        ('Venus', ephem.Venus()),
        ('Mars', ephem.Mars()),
        ('Jupiter', ephem.Jupiter()),
        ('Saturn', ephem.Saturn()),
        ('Uranus', ephem.Uranus()),
        ('Neptune', ephem.Neptune()),
        ('Pluto', ephem.Pluto())
    ]

    # Calculate and plot the positions of the celestial objects
    for name, obj in objects:
        obj.compute(birth_date, observer)
        ra = obj.ra / ephem.degree
        dec = obj.dec / ephem.degree
        ax.plot(ra, dec, 'o', markersize=8, label=name)

    # Set up the chart labels and title
    ax.set_xlabel('Right Ascension')
    ax.set_ylabel('Declination')
    ax.set_title('Astrology Natal Chart')

    # Set up the chart legend
    ax.legend()

    # Save the chart as an image
    image_path = 'natal_chart.png'
    plt.savefig(image_path)

    # Close the chart figure
    plt.close(fig)

    return image_path

# Example usage:
birth_date = datetime.datetime(1990, 1, 1, 12, 0, 0)  # Replace with the actual birth date and time
latitude = 51.5074  # Replace with the actual latitude of the birth location
longitude = -0.1278  # Replace with the actual longitude of the birth location

natal_chart_image = generate_natal_chart(birth_date, latitude, longitude)
print("Astrology natal chart image generated:", natal_chart_image)