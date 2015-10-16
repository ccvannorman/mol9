$(document).ready(function() {
	$("#buylesson").click(function(e) {
		base.buyPopup($("#buylesson").attr("data"), function() {
            base.popup("#postPurchasePopup");
            $("#postPurchasePopupContent").html("upgradedddd");
        });
	});	
});