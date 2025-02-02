import {Injectable} from '@angular/core';
import {SessionStorage} from "ngx-store";
import {Subject} from "rxjs";

/**
 * Service storing user preferences (in session storage for persistence).
 */
@Injectable({
	providedIn: 'root'
})
export class UiService {

	@SessionStorage({key: 'showHistory'})
	public showHistory: boolean = true;
	@SessionStorage({key: 'showOnlySums'})
	public showOnlySums: boolean = false;
	@SessionStorage({key: 'showImages'})
	public showImages: boolean = true;
	@SessionStorage({key: 'showNotifications'})
	public showNotifications: boolean = true;
	@SessionStorage({key: 'darkmode'})
	public darkmode: boolean = true;
	//public darkmode: boolean = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
	public darkmodeChanges = new Subject<boolean>();

	constructor() {
		this.setDarkmode(this.darkmode);
	}

	setDarkmode(enabled: boolean) {
		if (enabled) {
			document.body.parentElement.classList.add('dark');
		} else {
			document.body.parentElement.classList.remove('dark');
		}
		if (enabled != this.darkmode) {
			this.darkmodeChanges.next(enabled);
		}
		this.darkmode = enabled;
	}
}
