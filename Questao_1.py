class Report:
    def __init__(self, data_source):
        self.data_source = data_source

    def fetch_data(self):
        return self.data_source.read()

    def generate(self):
        result = self.fetch_data()
        return f"Report: {result}"


class ReportSaver:
    def save(self, report, filename):
        with open(filename, "w") as file:
            file.write(report)


class ReportSender:
    def send_by_email(self, report, email_address):
        print(f"Sending report to {email_address}: {report}")


class ReportGenerator:
    def __init__(self, data_source, saver=None, sender=None):
        self.report = Report(data_source)
        self.saver = saver if saver != None else ReportSaver()
        self.sender = sender if sender != None else ReportSender()

    def generate_report(self):
        return self.report.generate()

    def save_report(self, report, filename):
        self.saver.save(report, filename)

    def send_report_by_email(self, report, email_address):
        self.sender.send_by_email(report, email_address)
