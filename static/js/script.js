if(!Event.prototype.preventDefault){
	Event.prototype.preventDefault = function(){this.returnValue=false;};
}
if(!Event.prototype.stopPropagation){
	Event.prototype.stopPropagation = function(){this.cancelBubble=true;};
}

var App = (function(){
	"use strict";
	var ajax, cfg, instance;

	function App(){
		if(instance == null){
			instance = Object.create(App.prototype);

			cfg = {addEvent: 0, initialized: 0};

			if(Element.prototype.addEventListener) cfg.addEvent = 1;
			else if(Element.prototype.attachEvent){
				Element.prototype.addEventListener = function(eventName, listener, useCapture){
					this.attachEvent('on' + eventName, listener);
				}

				Element.prototype.removeEventListener = function(eventName, listener){
					this.detachEvent('on' + eventName, listener);
				}
				cfg.addEvent = 1;
			}

			ajax = {pages: [], content: [], xmls: [], baseurl: "", gen: null, run: false};
			if(window.XMLHttpRequest){/* code for IE7+, Firefox, Chrome, Opera, Safari */
				ajax.gen = function(){return new XMLHttpRequest();}
			} else /* code for IE6, IE5 */
				ajax.gen = function(){return new ActiveXObject("Microsoft.XMLHTTP");}

			ajax.baseurl = getUrl();
		}

		return instance;
	}

	function setUp(args){

	}
	function getUrl(){
		var url = "http://localhost:8000/";
		/*if(!window.location.origin){
		url = window.location.protocol +"//"+ window.location.host;
		} else url = window.location.origin;
		if(url === null || !(url) || (typeof url==='string' && url == 'null')) url = "";

		rrs = /\/$/.test(url);
		if(!rrs) url = url + "/";*/
		return url;
	}

	function getByID(id_str){
		var result;
		try {
			result = document.getElementById(id_str);
		}catch(e){result=null;}
		return result;
	}

	function isNumber(value){
		return ( Object.prototype.toString.call(value)!=='[object Array]' && (value-parseFloat(value)+1)>=0)?true:false;
	}
	function isString(str){
		var result = false;
		if( typeof str == "string" || (typeof st == "object" && st.constructor === String) ) result = true;
		if(result === true && str.length == 0) result = false;
		return result;
	}

	function clearNode(node){
		while(node.firstChild) node.removeChild(node.firstChild);
	}

	function contentArray(keys, values){
		var count = Math.min(keys.length, values.length), result = [];
		count = parseInt(count, 10);

		var i, key, val;
		for(i = 0; i < count; i++){
			key = encodeURIComponent( keys[i] );
			val = encodeURIComponent(values[i]);
			result.push(key + "=" + val);
		}
		return result;
	}

	function ajaxShift(){
		ajax.pages.shift();
		ajax.content.shift();
		ajax.xmls.shift();
		ajax.methods.shift();

		if(ajax.pages.length > 0 && ajax.content.length > 0 && ajax.xmls.length > 0) setTimeout(ajaxSend, 20);
		else ajax.run = false;
	}

	function newAjax(function1, function2){
		var xmlht = ajax.gen();

		xmlht.onreadystatechange = function(){
			if(xmlht.readyState == 4 && xmlht.status == 200){
				var result = xmlht.responseText, arr;
				if(result.substring(0, 9) == "for(;;) ;") result = result.substring(9);
				try {
					arr = JSON.parse(result);
				}catch(e){
					arr={};}
				function1(arr);
			} else if(xmlht.readyState == 4){
				function2();
			}
		};

		return xmlht;
	}

	function ajaxSend(){
		ajax.run = true;

		var xmlhttp = ajax.xmls[0], content = ajax.content[0], urlcp = ajax.pages[0];
		if(urlcp.substring(0, 4) != "http") urlcp = ajax.baseurl + ajax.pages[0];

		xmlhttp.open("POST", urlcp, true);
		xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
		xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
		xmlhttp.send(content);
	}

	function run(){
		if(cfg.initialized > 0) return;
		cfg.initialized += 1;

	}

	return {
		getInstance: function(){
			return new ApiWars();
		},
		init: function(){
			var inst2 = instance;
			if(instance == null) inst2 = new ApiWars();

			setUp({});
			run();

			return inst2;
		}
	}
})();

Object.freeze(ApiWars);

