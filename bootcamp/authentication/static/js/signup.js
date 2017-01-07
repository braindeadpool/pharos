function toggleFields() {
	console.log('This funtion was called');
	l = ['field_stu[]', 'university[]', 'room[]', 'city[]', 'state[]', 'country[]', 'device_name[]', 'description[]'];
	var arrayLength = l.length;
	
    if ($("#id_role").val() == 'Lab Manager'){
    	console.log('Showing');
        $("#parentPermission").show();
        for (var j = 0; j < arrayLength; j++) {
        	var x  = document.getElementsByName(l[j]);
        	for (i = 0; i < x.length; i++) {
        	   x[i].required = true;
        	}
        }
    }
    else{
        $("#parentPermission").hide();
        console.log('Hiding');
        for (var j = 0; j < arrayLength; j++) {
        	var x  = document.getElementsByName(l[j]);
        	for (i = 0; i < x.length; i++) {
        	   x[i].required = false;
        	}
        }
    }
}