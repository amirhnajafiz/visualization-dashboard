// === Global Variables ===
var all_countries = [];
var locationIDMap = { "world": "World" };

var pcp_countries = [];
var worldmap_country = "world";
var selected_attr = "anxiety";  // default music/mental health metric

var selected_countries = [];
var clicked_countries = []
var maxPCPCountry = 0;
var currLine = "none";


// === Trigger Handlers ===
function createTrigger() {
    return {
        aInternal: null,
        aListener: function(val) {},
        set a(val) {
            this.aInternal = val;
            this.aListener(val);
        },
        get a() {
            return this.aInternal;
        },
        registerListener: function(listener) {
            this.aListener = listener;
        }
    };
}

var lineChartTrigger = createTrigger();
var worldMapTrigger = createTrigger();
var worldMapTrigger2 = createTrigger();
var worldMapTrigger3 = createTrigger();
var pcpTrigger = createTrigger();
var statsTrigger = createTrigger();
var statsTrigger2 = createTrigger();

