import { BrowserModule, Title } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RouterModule, Routes } from '@angular/router';

import {MatToolbarModule} from '@angular/material/toolbar';
import {MatCardModule} from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatListModule} from '@angular/material/list';
import {MatDividerModule} from '@angular/material/divider';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatInputModule} from '@angular/material/input';
import {MatSliderModule} from '@angular/material/slider';
import {MatSelectModule} from '@angular/material/select';
import {MatTabsModule} from '@angular/material/tabs';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatNativeDateModule} from '@angular/material';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatTableModule} from '@angular/material/table';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatSortModule} from '@angular/material/sort';
import {MatRadioModule} from '@angular/material/radio';

import { HttpClientModule } from '@angular/common/http';
import { ViewMeetingComponent } from './view-meeting/view-meeting.component';
import { MeetingComponent } from './meeting/meeting.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { OverviewComponent } from './overview/overview.component';

import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { CustomerComponent } from './customer/customer.component';
import { ImprintComponent } from './imprint/imprint.component';
import { SetupComponent } from './setup/setup.component';

import { CookieService } from 'ngx-cookie-service';
import { AdministratorComponent } from './administrator/administrator.component';

const appRoutes: Routes = [
  { path: 'meeting/:uuid', component: MeetingComponent },
  { path: 'meeting/:uuid/:customer', component: MeetingComponent },
  { path: 'customer/:uuid', component: CustomerComponent },
  { path: 'imprint', component: ImprintComponent },
  { path: 'setup', component: SetupComponent },
  { path: 'admin', component: AdministratorComponent },
  { path: '', component: OverviewComponent },
  { path: ':uuid', component: OverviewComponent },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    ViewMeetingComponent,
    MeetingComponent,
    PageNotFoundComponent,
    OverviewComponent,
    CustomerComponent,
    ImprintComponent,
    SetupComponent,
    AdministratorComponent,
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    MatToolbarModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatGridListModule,
    MatListModule,
    MatDividerModule,
    MatSnackBarModule,
    MatInputModule,
    MatSliderModule,
    MatSelectModule,
    MatTabsModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatCheckboxModule,
    MatSliderModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatRadioModule,
    FormsModule,
    RouterModule.forRoot(
      appRoutes,
    )
  ],
  providers: [
    Title,
    CookieService,
  ],
  bootstrap: [AppComponent],
  exports: [
      MatSortModule,
  ],
})
export class AppModule { }
