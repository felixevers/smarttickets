import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import {SelectionModel} from '@angular/cdk/collections';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';

import {FormControl} from '@angular/forms';
import {DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE} from '@angular/material/core';
import {MatSort, MatTableDataSource} from '@angular/material';

import * as data from '../endpoint.json';

@Component({
  selector: 'app-administrator',
  templateUrl: './administrator.component.html',
  styleUrls: ['./administrator.component.css'],
})
export class AdministratorComponent implements OnInit {

  token: string;
  headers;

  meetings = [];
  prices = [];
  rooms = [];

  selectedMeeting;
  selectedPrice;
  selectedRoom;
  selectedSeat;
  selectedCustomer;

  selectedCustomerTickets = [];
  selectedCustomerSelectedTickets = new SelectionModel(true, []);

  selectedMeetingDate = new Date();
  selectedMeetingSaleStart = new Date();
  selectedMeetingSaleStop = new Date();
  selectedMeetingSaleStopTime = 0;
  selectedMeetingSaleStartTime = 0;
  selectedMeetingDateTime = 0;

  firstname: string = '';
  lastname: string = '';
  password: string = '';

  meetingName: string = '';
  meetingDescription: string = '';
  meetingSaleStart = new Date();
  meetingSaleStartTime = 0;
  meetingSaleStop = new Date();
  meetingSaleStopTime = 0;
  meetingDate = new Date();
  meetingDateTime = 0;
  meetingRoom;

  priceName: string = '';
  priceDescription: string = '';
  priceValue;

  roomName: string = '';

  seatRow;
  seatBlock;
  seatType;

  settingKey: string = '';
  settingValue: string = '';
  settingBeforeValue: string = '';

  administratorFirstname: string = '';
  administratorLastname: string = '';
  administratorPassword: string = '';

  administratorChangePassword: string = '';
  administratorChangePassword2: string = '';

  loadedCustomers = [];
  dataSource;

  @ViewChild(MatSort) sort: MatSort;
  @ViewChild('tabGroup') tabGroup;

  customerDisplayedColumns: string[] = ['select', 'firstname', 'lastname', 'email', 'count', 'place', 'address']
  selectedCustomerDisplayedColumns: string[] = ['select', 'price', 'block', 'row', 'seat', 'amount', 'paid'];

  times = [];

  constructor(private cookieService: CookieService, private http: HttpClient) {
    this.token = this.cookieService.get("token");

    for(var h = 0; h < 24; h++) {
      for(var m = 0; m < 4; m++) {
        this.times.push({
          "value": h*60 + m * 15,
          "minute": String("0" + m * 15).slice(-2),
          "hour": String("0" + h).slice(-2),
        })
      }
    }

    let instance = this;

    if(this.token != null && this.token != "") {
      instance.init();
    } else {
      this.token = null;
    }
  }

  goToLink(url: string){
    window.open(data['endpoint'] + url, "_blank");
  }

  init() {
    let instance = this;
    instance.http.get(data["endpoint"] + 'administrator/session/', instance.getHeader()).subscribe(resp => {
        if(resp["firstname"] != null && resp["lastname"] != null) {
        instance.firstname = resp["firstname"];
        instance.lastname = resp["lastname"];

        instance.getMeetings();
        instance.getPrices();
        instance.getRooms();
        instance.getCustomers();
      } else {
        instance.cookieService.set("token", "");
        instance.token = null;
      }
    });
  }

  ngOnInit() {
  }

  selectMeeting(meeting) {
    this.selectedMeeting = meeting;

    this.selectedMeetingDate = new Date(meeting.date * 1000);
    this.selectedMeetingDateTime = this.selectedMeetingDate.getMinutes();

    this.selectedMeetingSaleStart = new Date(meeting.start * 1000);
    this.selectedMeetingSaleStartTime = this.selectedMeetingSaleStart.getMinutes();

    this.selectedMeetingSaleStop = new Date(meeting.stop * 1000);
    this.selectedMeetingSaleStopTime = this.selectedMeetingSaleStop.getMinutes();
  }

  isAllSelected() {
    const numSelected = this.selectedCustomerSelectedTickets.selected.length;
    const numRows = this.selectedCustomerTickets.length;
    return numSelected === numRows;
  }

  masterToggle() {
    this.isAllSelected() ?
        this.selectedCustomerSelectedTickets.clear() :
        this.selectedCustomerTickets.forEach(row => this.selectedCustomerSelectedTickets.select(row));
  }

  calcAmountDue() {
    let amount = 0;

    this.selectedCustomerTickets.forEach(e => {
      if(!e.paid) {
        let price = this.getPrice(e.price_id);
        if(price != null) {
          amount += price.value;
        }
      }
    });

    return amount;
  }

  timeConverter(b) {
    let a = new Date(parseInt(b) * 1000);

    var year = a.getFullYear();
    var month = String("0" + (a.getMonth() + 1)).slice(-2);
    var date = String("0" + a.getDate()).slice(-2);
    var hour = String("0" + a.getHours()).slice(-2);
    var min = String("0" + a.getMinutes()).slice(-2);

    var time = date + '.' + month + '.' + year + ' um ' + hour + ':' + min + ' Uhr'

    return time;
  }

  calcSelectedAmountDue() {
    let amount = 0;

    this.selectedCustomerSelectedTickets.selected.forEach(e => {
      if(!e.paid) {
        amount += this.getPrice(e.price_id).value;
      }
    });

    return amount;
  }

  paySelected(pay) {
    let instance = this;

    var uuids = [];

    instance.selectedCustomerSelectedTickets.selected.forEach(ticket => {
      uuids.push(ticket["uuid"]);
    });

    instance.http.post(data["endpoint"] + 'ticket/pay/', {
      "tickets": uuids,
      "pay": pay,
    }, instance.getHeader()).subscribe(resp => {
    });

    instance.selectedCustomer = null;
    instance.selectedCustomerSelectedTickets = new SelectionModel(true, []);;
    instance.selectedCustomerTickets = [];
  }

  private loadTickets() {
    let instance = this;
    instance.http.post(data["endpoint"] + 'ticket/customer/' + instance.selectedCustomer.uuid, {}).subscribe(resp => {
      instance.selectedCustomerTickets = resp["tickets"];
      console.log(resp["tickets"]);
    });
  }

  getHeader() {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Token': this.token,
      }),
    };

    return httpOptions;
  }

  signInError() {
    this.firstname = '';
    this.lastname = '';
    this.password = '';
  }

  signIn() {
    let instance = this;

    instance.http.put(data["endpoint"] + 'administrator/session/', {
      "firstname": instance.firstname,
      "lastname": instance.lastname,
      "password": instance.password,
    }).subscribe(resp => {
      if(resp["result"] != null && !resp["result"]) {
        instance.signInError();
      } else {
        instance.token = resp["uuid"];
        instance.cookieService.set("token", instance.token);

        instance.init();
      }
    });
  }

  private getPrice(uuid) {
    let instance = this;
    let result = null;

    instance.prices.forEach(e => {
      if(e.uuid == uuid) {
        result = e;
      }
    });

    return result;
  }

  private createMeeting() {
    let instance = this;

    this.updateTime();

    instance.http.put(data["endpoint"] + 'meeting/', {
      "name": instance.meetingName,
      "description": instance.meetingDescription,
      "room": instance.meetingRoom, // TODO EDIT!
      "date": (instance.meetingDate.getTime() / 1000),
      "start": (instance.meetingSaleStart.getTime() / 1000),
      "stop": (instance.meetingSaleStop.getTime() / 1000),
    }, instance.getHeader()).subscribe(resp => {
      instance.meetingName = '';
      instance.meetingDescription = '';
      instance.meetingRoom = null;
      instance.meetingDate = null;
      instance.meetingSaleStart = null;
      instance.meetingSaleStop = null;
      instance.meetingSaleStopTime = 0;
      instance.meetingSaleStartTime = 0;
      instance.meetingDateTime = 0;

      instance.getMeetings();
    });
  }

  private disableMeeting() {
    return this.meetingName == '' || this.meetingName == null || this.meetingDescription == '' || this.meetingDescription == null || this.meetingRoom == '' || this.meetingRoom == null;
  }

  private createPrice() {
    let instance = this;

    instance.http.put(data["endpoint"] + 'price/', {
      "name": instance.priceName,
      "description": instance.priceDescription,
      "value": instance.priceValue,
    }, instance.getHeader()).subscribe(resp => {
      instance.priceName = '';
      instance.priceDescription = '';
      instance.priceValue= 0;
      instance.getPrices();
    });
  }

  private disablePrice() {
    return this.priceName == '' || this.priceName == null || this.priceDescription == '' || this.priceDescription == null || this.priceValue == null;
  }

  private createRoom() {
    let instance = this;
    instance.http.put(data["endpoint"] + 'room/', {
      "name": instance.roomName,
    }, instance.getHeader()).subscribe(resp => {
      instance.roomName = '';
      instance.getRooms();
    });
  }

  private disableRoom() {
    return this.roomName == '' || this.roomName == null;
  }

  private createSeat() {
    let instance = this;

    instance.http.put(data["endpoint"] + 'seat/', {
      "room": instance.selectedRoom.uuid,
      "block": instance.seatBlock - 1,
      "row": instance.seatRow - 1,
      "type": instance.seatType,
    }, instance.getHeader()).subscribe(resp => {
    });
  }

  private disableSeat() {
    return this.seatBlock == null || this.seatRow == null || this.seatType == null;
  }

  private getRooms() {
    let instance = this;

    instance.rooms = [];

    instance.http.get(data["endpoint"] + 'room/').subscribe(resp => {
      [].concat(resp).forEach(e => {
        instance.rooms.push(e);
      })
    });
  }

  private getCustomers() {
    let instance = this;

    instance.loadedCustomers = [];

    instance.http.get(data["endpoint"] + 'customer/', instance.getHeader()).subscribe(resp => {
      instance.loadedCustomers = resp["customers"];
      instance.dataSource = new MatTableDataSource(instance.loadedCustomers);
      instance.dataSource.sort = instance.sort;
    });
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  private getPrices() {
    let instance = this;

    instance.prices = [];

    instance.http.get(data["endpoint"] + 'price/').subscribe(resp => {
      instance.prices = resp["prices"];
    });
  }

  private getMeetings() {
    let obj = this;

    this.meetings = [];

    this.http.get(data["endpoint"] + "meeting/").subscribe(
      resp => {
        let list = resp["meetings"];

        if(list != null) {
          list.forEach(function(uuid) {
            obj.getMeeting(uuid).subscribe(
              resp => {
                if(resp != null) {
                  obj.meetings.push(resp);
                }
              }
            );;
          });
        }
      }
    );
  }

  private getMeeting(uuid) {
    return this.http.get(data["endpoint"] + "meeting/" + uuid);
  }

  signInDisabled() {
    return this.firstname == '' || this.lastname == '' || this.password == '';
  }

  private refreshSetting() {
    let instance = this;

    instance.http.get(data["endpoint"] + 'setting/' + instance.settingKey).subscribe(resp => {
      instance.settingBeforeValue = resp["value"];
      instance.settingValue = resp["value"];
    });
  }

  private updateTime() {
    this.meetingSaleStop.setHours(Math.floor(this.meetingSaleStopTime / 60));
    this.meetingSaleStop.setMinutes(this.meetingSaleStopTime % 60);
    this.meetingSaleStart.setHours(Math.floor(this.meetingSaleStartTime / 60));
    this.meetingSaleStart.setMinutes(this.meetingSaleStartTime % 60);
    this.meetingDate.setHours(Math.floor(this.meetingDateTime / 60));
    this.meetingDate.setMinutes(this.meetingDateTime % 60);
    this.selectedMeetingSaleStop.setHours(Math.floor(this.selectedMeetingSaleStopTime / 60));
    this.selectedMeetingSaleStop.setMinutes(this.selectedMeetingSaleStopTime % 60);
    this.selectedMeetingSaleStart.setHours(Math.floor(this.selectedMeetingSaleStartTime / 60));
    this.selectedMeetingSaleStart.setMinutes(this.selectedMeetingSaleStartTime % 60);
    this.selectedMeetingDate.setHours(Math.floor(this.selectedMeetingDateTime / 60));
    this.selectedMeetingDate.setMinutes(this.selectedMeetingDateTime % 60);
  }

  private updateSetting() {
    let instance = this;

    instance.http.post(data["endpoint"] + 'setting/', {
      "key": instance.settingKey,
      "value": instance.settingValue,
    }, instance.getHeader()).subscribe(resp => {
      if(resp["result"] != null && !resp["result"]) {
        instance.http.put(data["endpoint"] + 'setting/', {
          "key": instance.settingKey,
          "value": instance.settingValue,
        }, instance.getHeader()).subscribe(resp => {
          instance.settingBeforeValue = instance.settingValue;
        });
      } else {
        instance.settingBeforeValue = instance.settingValue;
      }
    });
  }

  private disableSetting() {
    return this.settingKey == '' || this.settingKey == null || this.settingValue == this.settingBeforeValue;
  }

  private generatePassword() {
    var length = 16,
        charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        retVal = "";
    for (var i = 0, n = charset.length; i < length; ++i) {
        retVal += charset.charAt(Math.floor(Math.random() * n));
    }
    return retVal;
  }

  private createAdministrator() {
    let instance = this;

    instance.http.post(data["endpoint"] + 'administrator/', {
      "firstname": instance.administratorFirstname,
      "lastname": instance.administratorLastname,
      "password": instance.administratorPassword,
    }, instance.getHeader()).subscribe(resp => {
      instance.administratorFirstname = '';
      instance.administratorLastname = '';
      instance.administratorPassword = '';
    });
  }

  private disableAdministrator() {
    return this.administratorFirstname == '' || this.administratorFirstname == null || this.administratorLastname == '' || this.administratorLastname == null;
  }

  private changeAdminstratorPassword() {
    let instance = this;
  }

  private disableChangeAdminstratorPassword() {
    return this.administratorChangePassword == '' || this.administratorChangePassword == null || this.administratorChangePassword2 == '' || this.administratorChangePassword2 == null || this.administratorChangePassword != this.administratorChangePassword2;
  }

  private update() {
    let instance = this;
    let i = this.tabGroup.selectedIndex;

    if(instance.selectedPrice != null && i == 2) {
      instance.http.post(data["endpoint"] + 'price/' + instance.selectedPrice.uuid, {
        "name": instance.selectedPrice.name,
        "description": instance.selectedPrice.description,
        "value": instance.selectedPrice.value,
      }, instance.getHeader()).subscribe(resp => {
        instance.selectedPrice = null;
        instance.getPrices();
      });
    }
    if(instance.selectedMeeting != null && i == 1) {
      instance.updateTime();

      instance.http.post(data["endpoint"] + 'meeting/' + instance.selectedMeeting.uuid, {
        "name": instance.selectedMeeting.name,
        "description": instance.selectedMeeting.description,
        "room": instance.selectedMeeting.room,
        "date": (instance.selectedMeetingDate.getTime() / 1000),
        "start": (instance.selectedMeetingSaleStart.getTime() / 1000),
        "stop": (instance.selectedMeetingSaleStop.getTime() / 1000),
      }, instance.getHeader()).subscribe(resp => {
        instance.selectedMeeting = null;
        instance.selectedMeetingDate = new Date();
        instance.selectedMeetingSaleStart = new Date();
        instance.selectedMeetingSaleStop = new Date();
        instance.selectedMeetingSaleStopTime = 0;
        instance.selectedMeetingSaleStartTime = 0;
        instance.selectedMeetingDateTime = 0;

        instance.getMeetings();
      });
    }
  }

  private delete() {
    let instance = this;
    let i = this.tabGroup.selectedIndex;

    if(instance.selectedPrice != null && i == 2) {
      instance.http.delete(data["endpoint"] + 'price/' + instance.selectedPrice.uuid, instance.getHeader()).subscribe(resp => {
        instance.selectedPrice = null;
        instance.getPrices();
      });
    }
    if(instance.selectedRoom != null && i == 3) {
      instance.http.delete(data["endpoint"] + 'room/' + instance.selectedRoom.uuid, instance.getHeader()).subscribe(resp => {
        instance.selectedRoom = null;
        instance.getRooms();
      });
    }
    if(instance.selectedMeeting != null && i == 1) {
      instance.http.delete(data["endpoint"] + 'meeting/' + instance.selectedMeeting.uuid, instance.getHeader()).subscribe(resp => {
        instance.selectedMeeting = null;
        instance.getMeetings();
      });
    }
    if(instance.selectedCustomer != null && i == 4) {
      instance.http.delete(data["endpoint"] + 'customer/' + instance.selectedCustomer.uuid, instance.getHeader()).subscribe(resp => {
        instance.selectedCustomer = null;
        instance.getCustomers();
      });
    }
  }

  deleteTicket() {
    let instance = this;
    let i = this.tabGroup.selectedIndex;

    if(instance.selectedCustomerSelectedTickets.selected.length > 0 && i == 4) {
      instance.selectedCustomerSelectedTickets.selected.forEach(e => {
        instance.http.delete(data["endpoint"] + 'ticket/' + e.uuid, {}).subscribe(resp => {
          instance.selectedCustomer = null;
          instance.selectedCustomerSelectedTickets = new SelectionModel(true, []);;
          instance.selectedCustomerTickets = [];
        });
      });
    }
  }

}
