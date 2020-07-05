import sys
import traceback


class ExecuteUserScript(object):
    def __init__(self, configOptions, logs):
        self.configOptions = configOptions
        self.logs = logs

    def captureTraceback(self):
        """Display the exception that just occurred.

        return:
            list with the traceback

        """
        try:
            type, value, tb = sys.exc_info()
            sys.last_type = type
            sys.last_value = value
            sys.last_traceback = tb
            tblist = traceback.extract_tb(tb)
            del tblist[:1] # removing AutoBugTracker stack line
            tracebackList = traceback.format_list(tblist)
            if tracebackList:
                tracebackList.insert(0, "Traceback (most recent call last):\n")
            tracebackList[len(tracebackList):] = traceback.format_exception_only(type, value)
        finally:
            tblist = tb = None
        return tracebackList

    def executeScript(self, scriptName):
        """ Execute parent program

            execute user script, takes script to execute as an argument
            either graceful execution or bug information such as capturing traceback

        Return:
             list of traceback stack if user program crash

        """
        try:
            return exec(open(scriptName).read())
        except FileNotFoundError:
            print(f'{scriptName} script is not found!')
            self.logs.writeToFile(message=self.captureTraceback())
        except ModuleNotFoundError as e:
            print(f'{e}, module is not found!')
            self.logs.writeToFile(message=self.captureTraceback())
            # Blacklist the script with missing module and notify user. Do not submit Bug!
        except:
            print(f'{scriptName} did not exit gracefully, Submit a Bug!"')
            return self.captureTraceback()
