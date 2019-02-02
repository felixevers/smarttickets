import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

@NgModule({
  declarations: [],
  imports: [
    CommonModule
  ]
})
export class ApiModule {

  static https: boolean = false;
  static host: string = "localhost";
  static port: string = "5000";

  public static getURL() {
    var protocol = this.https ? "https://" : "http://";

    return protocol + this.host + ":" + this.port + "/";
  }

}
