import os

from models import ApplicationLogProxy, ApplicationProxy, CategoryProxy, UserProxy
from django.test import TestCase
from unittest import TestLoader, TextTestRunner

from settings import APPS_MAX_LOG_ENTRIES, relative
from mtmenu import application_running

class TestMultiTouch(TestCase):
    """ Tests defined to the Wall Application 
    NOTE: Some tests take several time sleeping to assure the system calls are performed
    before the test asserts """

    def setUp(self):
        """ Sets up the database to have one user and one application """
        self.user = UserProxy.objects.create(username = "username",
                                             email = "username@email.com",
                                             password = "password")
        self.games = CategoryProxy.objects.create(name="GamesCategory")
        self.tetris = ApplicationProxy.objects.create(name="Tetris Game App",
                                                      owner=self.user,
                                                      category=self.games)
                                                      
        folder = relative('./apps/%s' % self.tetris.id)
        if not os.path.exists(folder):
            os.mkdir(folder)
            import platform
            if platform.system()[:3].lower() == "win":
                boot_txt = "notepad.exe"
            else:
                boot_txt = "python -c 'raw_input()'"
            open(os.path.join(folder,'boot.bat'), 'w').write(boot_txt)
            self.created_test_app = folder
        else:
            self.created_test_app = False

    def test_application_log_add (self):
        """ Tests to add some log messages to an application log """
        log_message1 = "Log message 1 (one)"
        log_message2 = "Log message 2 (two)"
        self.tetris.add_log_entry(log_message1)
        self.tetris.add_log_entry(log_message2)
        
        logs = ApplicationLogProxy.objects.filter(application = self.tetris)
        
        self.assertEqual(logs[logs.count() - 1].error_description, log_message2)
    
    def test_run_application(self):
        """ Tests running an application """
        self.tetris.execute()
        
        import time
        time.sleep(5)
        
        import application_running
        app = application_running.getAppRunning()
        
        self.assertNotEqual(app, None)
        self.assertEqual(app.poll(), None)
    
    
    def test_terminate_application(self):
        """ Kills the running application (if none runnig, it starts it) """
        import application_running
        import time
        
        if not application_running.isAppRunning():
            self.tetris.execute()
            time.sleep(5)
            
        app = application_running.getAppRunning()
        
        # guarantee the application is running
        self.assertNotEqual(app, None)

        application_running.killAppRunning()
         
        time.sleep(5)
        
        self.assertNotEqual(app.poll(), None)
    
    def tearDown(self):
        if self.created_test_app:
            os.remove(os.path.join(self.created_test_app,'boot.bat'))
            os.rmdir(self.created_test_app)
    

if __name__ == '__main__':
    tests = TestLoader().loadTestsFromTestCase(TestMultiTouch)
    TextTestRunner(verbosity = 2).run(tests)
    