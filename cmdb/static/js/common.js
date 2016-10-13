$('#menu').find('li').each(function(){
	$(this).click(function(){
		$(this).siblings().removeClass('active');	
		$(this).addClass('active');
	})
})
