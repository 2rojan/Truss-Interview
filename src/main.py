import pandas as pd
import codecs, sys, io
from datetime import datetime


pd.set_option("display.max_rows", None, "display.max_columns", None)
sys.stdout.reconfigure(encoding='utf-8')


class Normalizer:

    def stream(input_stream):
        df = pd.read_csv(input_stream)


        def foobar(column, name, location):
            newSeries = pd.Series(name=name)
            try:
                for index, value in column.items():
                    newValue = convert_seconds(value)
                    a = pd.Series([newValue], index=[index], name=name)
                    newSeries = newSeries.append(a)
            except Exception:
                sys.stderr.write("Error converting time for {index} {value}")
            return newSeries

        # Convert HH:MM:SS.MS to seconds
        def convert_seconds(time):
            try:
                time = time.split(":")
                hour = int(time[0])
                minute = int(time[1])
                second = float(time[2])
                finalValue = (hour * 3600) + (minute * 60) + second
                return finalValue
            except ValueError:
                sys.stderr.write("Error converting times to seconds.")

        # Timestamp conversion. Assumed Pacific, convert to eastern. 
        # Note: Daylight Savings Time.
        # ToDo: this is doing blanket conversion. Change so only MISSING TZ info is converted. 
        try:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df['Timestamp'] = df['Timestamp'].dt.tz_localize('US/Pacific')
            df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern')
            
        except ValueError:
            sys.stderr.write("Error converting TimeZone from US/Pacific to US/Eastern")

        # Converts ZIP(zipcodes) to 5 digits with leading Zeros
        try:
            df['ZIP'] = df['ZIP'].apply(lambda x: '{0:0>5}'.format(x))
        except ValueError:
            sys.stderr.write("Error converting ZipCode to 5 digits")

        # Converts FullName to Uppercase. Check if another exception is suitable. 
        try:
            df['FullName'] = df['FullName'].str.upper()
        except OSError:
            sys.stderr.write("Error converting name to Uppercase")
        
        # foobar function to convert durations to seconds
        # Creates new Series to be inserted
        try:
            foo = df['FooDuration']
            bar = df['BarDuration']

            newFoo = foobar(foo, 'FooDuration', 4)
            newBar = foobar(bar, 'BarDuration', 5)
        except Exception:
            sys.stderr.write("Error converting Time")

        # deletes current series in anticipation of inserting new series created in foobar function
        try:
            del df['FooDuration']
            del df['BarDuration']
        except Exception:
            sys.stderr.write("Error deleting original Series")

        # Inserts New Series
        try:
            df.insert(4, 'FooDuration', newFoo)
            df.insert(5, 'BarDuration', newBar)
        except Exception:
            sys.stderr.write("Error inserting New Series with Converted Durations")
        
        #Adds Foo and Bar Durations into Total Durations Series
        try:
            df['TotalDuration'] = df['FooDuration'] + df['BarDuration']
        except Exception:
            sys.stderr.write("Error adding FooDuration and BarDuration columns for TotalDuration")

        # Write to stdout
        df.to_csv(sys.stdout, index=False)


