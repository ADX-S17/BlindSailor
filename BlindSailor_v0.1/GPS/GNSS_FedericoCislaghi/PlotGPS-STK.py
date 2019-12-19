import win32com.client

# Start new instance of STK
uiApplication = win32com.client.Dispatch('STK11.Application')
uiApplication.Visible = True

# Alternatively, uncomment the following lines to get a reference to a running STK instance
# uiApplication = win32com.client.GetActiveObject('STK11.Application')

# Get our IAgStkObjectRoot interface
root = uiApplication.Personality2

#root.NewScenario('Python_Test_Scenario')
satellite = root.CurrentScenario.Children.New(18, 'this_Satellite') # eSatellite

input("Press enter to exit script.")
