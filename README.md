# Qauto

<p>A project base on appium and selenium.</p>
<pre><code>It now supports for web/iOS/android, if you want to run your own auto test by it, 
just write the codes of your app in the file named '/platforms/*/methods.py' and 
import them at '/platforms/*/__init__.py'.
</code></pre>



# Run
<pre><code>After changing the settings of appium session or selenium 
execuatable_path in manage.py, execute the commands such as: 
> python manage.py web steps.csv
> python manage.py ios steps.csv
> python manage.py android steps.csv
Then manage.py will run the method named 'run' in platfroms/*/__init__.py
</code></pre>
