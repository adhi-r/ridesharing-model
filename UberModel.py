import matplotlib.pyplot as plt
#%matplotlib inline
import random 
import numpy as np
from IPython.display import display, clear_output
import time
import math

class driver():
    """Creates a driver capable of picking up riders and taking them to their destination. Drivers may only have 1 rider at a
    time. """
    
    def __init__(self, x_dim, y_dim):
        """Defines a driver whose default location is randomly located within the dimensions of the world and who hasn't been
        hired and doesn't have a rider in their vehicle."""
        self.location = [np.random.randint(0,x_dim), np.random.randint(0,y_dim)]
        self.has_rider = False   # True when rider is in their car
        self.my_rider = "None"   # Corresponds to rider from when the rider selects the driver until they've been dropped off.
        
    def move(self):
        """If the driver has a job, this moves the driver one position closer to their destination or picks up the rider. 
        (If they haven't picked up the rider yet, then their destination is the rider's location. If they 
        have picked up the rider, then their destination is the rider's destination.) The driver first will move right/left, and
        then up/down. (Note: Drivers do not pick up or drop off their passenger and move in the same iteration (i.e. Drivers will
        spend one iteration obtaining their rider.))
        """

        if self.my_rider != "None":       
            if self.has_rider == False:
                if self.location[0] < self.my_rider.location[0]:
                    self.location[0] += 1
                elif self.location[0] > self.my_rider.location[0]:
                    self.location[0] -= 1
                else:
                    if self.location[1] < self.my_rider.location[1]:
                        self.location[1] += 1
                    elif self.location[1] > self.my_rider.location[1]:
                        self.location[1] -= 1
                    else:
                        self.has_rider = True
            elif self.has_rider == True:
                if self.location[0] < self.my_rider.destination[0]:
                    self.location[0] += 1
                    self.my_rider.location[0] += 1
                elif self.location[0] > self.my_rider.destination[0]:
                    self.location[0] -= 1
                    self.my_rider.location[0] -= 1
                else:
                    if self.location[1] < self.my_rider.destination[1]:
                        self.location[1] += 1
                        self.my_rider.location[1] += 1
                    elif self.location[1] > self.my_rider.destination[1]:
                        self.location[1] -= 1
                        self.my_rider.location[1] -= 1                                          
        
    def draw(self):
        """Plots the driver green if they have a rider, red if they don't have a rider."""
        color = 'r'
        if (self.has_rider == True):
            color = 'g'
        plt.scatter(self.location[0], self.location[1], s = 150, color=color);
                
        
class rider():
    """Creates a driver capable of picking up riders and taking them to their destination. Drivers may only have 1 rider at a
    time. Once assigned to a rider, a driver will their rider directly to their destination immediately."""
    
    def __init__(self, x_dim, y_dim):
        """Defines a rider whose default location is randomly located within the dimensions of the world, who has a
        destination at another location, and who has no driver."""    
        self.location = [np.random.randint(0,x_dim), np.random.randint(0,y_dim)]
        self.destination = [np.random.randint(0,x_dim), np.random.randint(0,y_dim)]
        # Prevents the possibility that the location and destination are the same
        while self.destination == self.location: 
            self.destination = [np.random.randint(0,x_dim), np.random.randint(0,y_dim)]
        self.wait_time = 0    # amount of time rider waits after driver has been selected until they're picked up
        self.ride_time = 0    # amount of interations it takes to be driven to the destination
        
        
    def closest_available_driver(self, available_drivers):
        """ Uses a a list of available drivers to calculate the distance between the rider and all available drivers and assigns
        the closest driver the following rider. Returns the closest driver and their location."""
        
        # Creates a list of driver locations.
        driver_locations = []
        for d in available_drivers:
            driver_locations.append(d.location)
            
        # Determines the nearest driver's location.
        shortest_dist = 99999
        for l in driver_locations:
            dist = math.sqrt( (l[0] - self.location[0])**2 + (l[1] - self.location[1])**2 )
            if dist < shortest_dist:
                shortest_dist = dist
                nearest_driver_location = l
        
        # Determines the nearest driver.
        for d in available_drivers:
            if d.location == nearest_driver_location:
                nearest_driver = d
                
        return nearest_driver, nearest_driver_location
    
    def draw(self):
        """Plots the rider yellow."""
        plt.scatter(self.location[0], self.location[1], s = 150, color='y')
    
        
def run(num_drivers = 10, rider_spawn_prob = 0.3, x_dim = 70, y_dim = 70, iterations = 100, vis = True):
    """Creates a world of size x_dim by y_dim with the specified number of drivers (red points) and if vis = True runs a 
    simulation in which riders (yellow points) and their destinations (red splotches) spawn according to the given rider spawn
    probability, riders select the closest driver, and said driver picks up the rider and drops them off at their destination.
    Returns a list of wait and ride times for the riders that were transported to their destination."""
    
    # Initializes an empty array for the world and sets the animation dimensions
    world = np.zeros((x_dim,y_dim))
    if vis == True:
        fig, ax = plt.subplots(figsize=(30,15));
        ax.set_axis_bgcolor('white')
    
    # Creates a list of drivers and available drivers
    drivers = [driver(x_dim,y_dim) for a in range(0,num_drivers)]
    available_drivers = []
    for d in drivers:
        available_drivers.append(d)
    
    # Creates an empty list for riders, rider wait times, and rider ride times
    riders = []
    rider_wait_times = []
    rider_ride_times = []
    dropped_riders = 0
    
    iterations_ran = 0
    
    while iterations_ran < iterations:
        
        if rider_spawn_prob > random.random():
            
            # A new rider & their destination spawn
            new_rider = rider(x_dim,y_dim)   
            riders.append(new_rider)
            world[tuple(new_rider.destination)] = 15
            
            # Assigns the closest available driver to the rider, if there is an available driver.
            if available_drivers != []:
                closest_driver, closest_driver_location = new_rider.closest_available_driver(available_drivers)
                closest_driver.my_rider = new_rider
                available_drivers.remove(closest_driver)
            else:
                world[tuple(new_rider.destination)] -= 15
                riders.remove(new_rider)
                dropped_riders += 1
                #print("No available driver. A rider may not have been assigned")
                
            """***The above block is a problem since it makes it so that if there isn't an available driver, the rider will 
            never get assigned to a driver."""
        
        # For each driver, if they have a job they move one step closer towards their destination.
        for d in drivers: 
            d.move()  
            
        # For each rider, adds 1 to their wait time if they're waiting or 1 to their ride time if they're being driven.
        for d in drivers:
            if d.my_rider != "None":
                if d.has_rider == False:
                    d.my_rider.wait_time += 1
                else:
                    d.my_rider.ride_time += 1
        
        # If a driver has the rider and is at their destination, drop the rider off and remove them from the animation.
        for d in drivers:
            if d.my_rider != "None":
                if d.my_rider.destination == d.location:
                    # Record wait and ride times to lists
                    rider_wait_times.append(d.my_rider.wait_time)
                    rider_ride_times.append(d.my_rider.ride_time)
                    # Driver drops rider off and remove them from the animation
                    riders.remove(d.my_rider)
                    world[tuple(d.my_rider.destination)] = 0
                    d.has_rider = False
                    d.my_rider = "None"
                    available_drivers.append(d)
                    
        iterations_ran += 1
        
        if vis == True:
            # Plots the world
            plt.imshow(world.T, origin='lower', aspect='equal');
            plt.text(x_dim - 10.5, y_dim - 2,'Iterations: %s' %iterations_ran, color='w', size = 15, horizontalalignment='left', verticalalignment='center')
            plt.text(x_dim - 14.7, y_dim - 4,'Dropped Riders: %s' %dropped_riders, color='w', size = 15, horizontalalignment='left', verticalalignment='center')

            for r in range(0,len(riders)):
                riders[r].draw()
            for d in range(0,num_drivers):
                drivers[d].draw()

            # Allows animation
            clear_output(wait=True) # Clear output for dynamic display
            display(fig)            # Reset display
            fig.clear()             # Prevent overlapping and layered plots
            time.sleep(0.0001)      # Sleep for a fraction of a second to allow animation to catch up
            
    return rider_wait_times, rider_ride_times, dropped_riders

def experiment(independent_variable = '', IV_vals = [], x_dim = 70, y_dim = 30, iterations = 100, vis = False):
    '''
    Conducts the experiment of the given parameters on the UberModel, and returns the data of the experiment
    in a form that makes analysis and plotting easy.
    
    The last six parameters are default parameters borrowed from the `run()` function and are passed 
    into the `run()` within the experiment. The default values are the same, save for `vis` which is 
    set to `False` by default to expedite the experiment.
    
    `independent_variable` must be a string, either "rider" or "driver".
    
    `IV_vals` must be a list of the tested values of the independent variable. For drivers this must
    be a list of integers. For riders it must be a list of values greater than 0 and less than 1.'''
    
    wait_times_per_IV = []
    ride_times_per_IV = []
    dropped_riders_per_IV = []
    
    wait_times_per_run = []
    ride_times_per_run = []
    dropped_riders_per_run = []
    
    # Check which experiment to do
    if str(independent_variable).lower() == 'driver':
        
        # Check if independent values make sense
        if False in [x % 1 == 0 for x in IV_vals]:
            raise ValueError('You are testing quantity of drivers, so only use integers in IV_vals.')
            
        # Run the model over each value of the independent variable list           
        for val in IV_vals:
            w, r, d = run(num_drivers = val, x_dim = x_dim, y_dim = y_dim, iterations = iterations, vis = vis)
            
            # Averaging the wait times of every rider in the run
            avg_w = sum(w)/len(w)
            avg_r = sum(r)/len(r)
            
            wait_times_per_run.append(avg_w)
            ride_times_per_run.append(avg_r)
            dropped_riders_per_run.append(d)
            
            # Averaging the average wait times of every rider of every run to get a value that corresponds with the IV
            wait_times_per_IV.append(sum(wait_times_per_run)/len(wait_times_per_run))
            ride_times_per_IV.append(sum(ride_times_per_run)/len(ride_times_per_run))
            dropped_riders_per_IV.append(sum(dropped_riders_per_run)/len(dropped_riders_per_run))
            
    if str(independent_variable).lower() == 'rider':
        
        # Check if independent values make sense
        if True in [x > 1 or x <= 0 for x in IV_vals]:
            raise ValueError('You are testing probability of rider spawn, so please only use floats between 0 and 1.')
            
        # Run the model over each value of the independent variable list           
        for val in IV_vals:
            w, r, d = run(rider_spawn_prob = val, x_dim = x_dim, y_dim = y_dim, iterations = iterations, vis = vis)
            
            # Averaging the wait times of every rider in the run
            avg_w = sum(w)/len(w)
            avg_r = sum(r)/len(r)
            #avg_d = 
            
            wait_times_per_run.append(avg_w)
            ride_times_per_run.append(avg_r)
            dropped_riders_per_run.append(d)
            
            # Averaging the average wait times of every rider of every run to get a value that corresponds with the IV
            wait_times_per_IV.append(sum(wait_times_per_run)/len(wait_times_per_run))
            ride_times_per_IV.append(sum(ride_times_per_run)/len(ride_times_per_run))
            dropped_riders_per_IV.append(sum(dropped_riders_per_run)/len(dropped_riders_per_run))
                                 
    
    return IV_vals, wait_times_per_IV, ride_times_per_IV, dropped_riders_per_IV