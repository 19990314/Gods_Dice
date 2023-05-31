import matplotlib.pyplot as plt

# Sample data
ages = [25, 30, 35, 40, 45]
events = ['Graduation', 'Marriage', 'Career Change', 'Parenthood', 'Retirement']

# Create the plot
plt.plot(ages, events, marker='o')
plt.xlabel('Age')
plt.ylabel('Life Event')
plt.title('Life Events by Age')
plt.grid(True)
plt.show()