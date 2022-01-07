from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
from collections import deque


change_oil_queue = deque()
inflate_tires_queue = deque()
diagnostic_queue = deque()
number_of_ticket = 0


class WelcomeView(View):
    template_name = "tickets/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"number_of_ticket": number_of_ticket})


class MenuView(View):
    template_name = "tickets/main_page.html"

    def get(self, request, *args, **kwargs):
        menu = {"change_oil": "Change oil",
                "inflate_tires": "Inflate tires",
                "diagnostic": "Diagnostic"}

        return render(request, self.template_name, {"menu": menu})


class QueueHandler(View):
    template_name = "tickets/ticket.html"
    tickets = []
    time_to_wait = []
    services = {"change_oil": {"queue": change_oil_queue, "time": 2},
                "inflate_tires": {"queue": inflate_tires_queue, "time": 5},
                "diagnostic": {"queue": diagnostic_queue, "time": 30}}

    def get(self, request, *args, **kwargs):
        service = kwargs["link"]
        ticket = self.get_new_ticket(service)
        return render(request, self.template_name, {"ticket_number": ticket, "minutes_to_wait": self.count_time(ticket, service)})

    def count_time(self, user_ticket, user_service):
        time_counter = 0
        if len(self.tickets) <= 2:
            self.time_to_wait.append(self.services[user_service]["time"])
            return time_counter
        if user_ticket == 3:
            return min(self.time_to_wait)
        for service in self.services.keys():
            time_counter += self.services[service]["time"] * len(self.services[service]["queue"])
            if user_ticket in self.services[service]["queue"]:
                time_counter -= self.services[service]["time"]
                break
        return time_counter

    def get_new_ticket(self, user_service):
        ticket = len(self.tickets) + 1
        self.tickets.append(ticket)
        self.services[user_service]["queue"].append(ticket)
        return ticket

    def dequeue(self, service):
        self.services[service]["queue"].popleft()


class ProcessingView(View):
    template_name = "tickets/operator_menu.html"

    def get(self, request, *args, **kwargs):
        context = {
            "change_oil": len(change_oil_queue),
            "inflate_tires": len(inflate_tires_queue),
            "diagnostic": len(diagnostic_queue)
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        global number_of_ticket
        if len(change_oil_queue) > 0:
            number_of_ticket = change_oil_queue[0]
            change_oil_queue.popleft()
        elif len(inflate_tires_queue) > 0:
            number_of_ticket = inflate_tires_queue[0]
            inflate_tires_queue.popleft()
        elif len(diagnostic_queue) > 0:
            number_of_ticket = diagnostic_queue[0]
            diagnostic_queue.popleft()
        else:
            number_of_ticket = 0
        return HttpResponseRedirect('/next/')


class NextView(View):
    template_name = "tickets/next.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"number_of_ticket": number_of_ticket})













