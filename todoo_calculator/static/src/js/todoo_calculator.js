odoo.define('todoo_calculator.calculator', function (require) {
    "use strict";

    var config = require('web.config');
    var core = require('web.core');
    var session = require('web.session');
    var time = require('web.time');
    var utils = require('web.utils');
    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu');

    var _t = core._t;
    var QWeb = core.qweb

    var CalculatorItem = Widget.extend({
        template:'todoo.CalculatorItem',
        events: {
            "click": "on_click",
            "keydown": "_onKeydown",

        },
        on_click: function (event) {
            if ($(event.target).is('i') === false) {
                event.stopPropagation();
            }
            //
            // var pressKey = event.target;
            // switch (pressKey.value) {
            //     case '1':
            //         console.log(pressKey);
            //     case '2':
            //         console.log(pressKey);
            //     case '3':
            //         console.log(pressKey);
            //     case '4':
            //         console.log(pressKey);
            //     case '5':
            //         console.log(pressKey);
            //     case '6':
            //         console.log(pressKey);
            //     case '7':
            //         console.log(pressKey);
            //     case '8':
            //         console.log(pressKey);
            //     case '9':
            //         console.log(pressKey);
            //     case '0':
            //         console.log(pressKey);
            //     case 'CE':
            //         console.log(pressKey);
            //     case 'C':
            //         console.log(pressKey);
            //     case '±':
            //         console.log(pressKey);
            //     case '%':
            //         console.log(pressKey);
            //     case '-':
            //         console.log(pressKey);
            //     case '.':
            //         console.log(pressKey);
            //     case '=':
            //         console.log(pressKey);
            //     case '+':
            //         console.log(pressKey);
            //     break;
            //     default:
            // }
        },
        _onKeydown: function(event) {
            console.log(event, 'Log event key');
        },
        keywrite: function (keyPress) {
            console.log(keyPress);
        }
    });

    SystrayMenu.Items.push(CalculatorItem);

    return {
        CalculatorItem: CalculatorItem,
    };


});