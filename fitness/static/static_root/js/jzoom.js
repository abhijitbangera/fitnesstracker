/*!
 * jZoom.js 1.1.4
 *
 * https://github.com/pciapcib/jZoom
 *
 * MIT licensed
 *
 * Copyright (c) 2016 Shen Ting
 */
(function($) {
    $.fn.jzoom = function(options) {
        return this.each(function() {
            //设置默认属性
            //Set up default options
            var defaultOptions = {
                width: 400,
                height: 400,
                position: "right",
                offsetX: 20,
                offsetY: 0,
                opacity: 0.6,
                bgColor: "#fff",
                loading: "Loading..."
            };

            //用户自定义属性
            //Custom options
            options = $.extend(true, defaultOptions, options);

            //获取容器，设置默认定位，并使图片的宽高与容器相同
            //Get container to add position and make the image having same width and height with container
            var $jzoom = $(this);
            var jzoomPosition = $jzoom.css('position');
            if (jzoomPosition === "static") {
                $jzoom.css('position', 'relative');
            }
            $jzoom.find('img').css({
                width: $jzoom.width() + "px",
                height: $jzoom.height() + "px"
            });

            //获取镜头div，设置样式，部分样式从属性设置中取得
            //Get lens div and add css
            var $jzoomLens = $('<div></div>');
            $jzoomLens.css({
                position: "absolute",
                zIndex: "990",
                opacity: defaultOptions.opacity,
                cursor: "move",
                border: "1px solid #ccc",
                backgroundColor: defaultOptions.bgColor
            });

            //获取放大镜div，设置样式，部分样式从属性设置中取得
            //Get zooming window and add css
            var $jzoomDiv = $('<div></div>');
            var jzoomDivLeft, jzoomDivTop;
            switch (defaultOptions.position) {
                case "top":
                    jzoomDivLeft = 0;
                    jzoomDivTop = -defaultOptions.height - defaultOptions.offsetY;
                    break;
                case "right":
                    jzoomDivLeft = $jzoom.width() + defaultOptions.offsetX;
                    jzoomDivTop = 0;
                    break;
                case "bottom":
                    jzoomDivLeft = 0;
                    jzoomDivTop = $jzoom.height() + defaultOptions.offsetY;
                    break;
                case "left":
                    jzoomDivLeft = -defaultOptions.width - defaultOptions.offsetX;
                    jzoomDivTop = 0;
                    break;
            }
            $jzoomDiv.css({
                left: jzoomDivLeft + "px",
                top: jzoomDivTop + "px",
                width: defaultOptions.width + "px",
                height: defaultOptions.height + "px",
                position: "absolute",
                zIndex: "999",
                overflow: "hidden",
                border: "1px solid #ccc",
                fontSize: "20px",
                textAlign: "center",
                lineHeight: defaultOptions.height + "px"
            });

            //获取大图，并设置后缀名和文件格式，与载入文字一起添加到容器中
            //Create <img> of big image and add loading text
            var $zoomImg = createZoomImg(defaultOptions.suffixName, defaultOptions.imgType);
            $jzoomDiv.append($zoomImg).append(defaultOptions.loading);

            //声明全局变量和常量
            //Variables
            var flag = 0,
                JzoomOffset = $jzoom.offset(),
                CriticalX, CriticalY,
                finalX, finalY,
                DistProportionX, DistProportionY;

            //添加鼠标事件
            //Mouse events
            $jzoom.mouseenter(function() {
                    $jzoomLens.show();
                    $jzoomDiv.show();
                    if (flag === 0) {
                        firstEnter();
                        flag++;
                    }
                })
                .mousemove(function(e) {
                    //计算镜头div坐标
                    //Calculate coordinates of lens div
                    finalX = calcDistance(e.pageX, JzoomOffset.left, $jzoomLens.width(), CriticalX);
                    finalY = calcDistance(e.pageY, JzoomOffset.top, $jzoomLens.height(), CriticalY);

                    $jzoomLens.css({
                        left: finalX + "px",
                        top: finalY + "px"
                    });

                    //计算大图的偏移坐标
                    //Calculate offsets of big images
                    $zoomImg.css({
                        left: -finalX * DistProportionX + "px",
                        top: -finalY * DistProportionY + "px"
                    });
                })
                .mouseleave(function() {
                    $jzoomLens.hide();
                    $jzoomDiv.hide();
                });

            /**
             * 创建大图
             * Create <img> of big image
             * @param  {String} suffixName 大图后缀 suffix name of big image
             * @param  {String} imgType    图片格式 image type of big image
             * @return {jQuery}            返回大图 big image
             */
            function createZoomImg(suffixName, imgType) {
                var imgSrc = $jzoom.find("img").attr("src");

                suffixName = suffixName || "_big";

                var point = imgSrc.lastIndexOf(".");

                imgType = imgType || imgSrc.substring(point + 1);

                var newImgSrc = imgSrc.substring(0, point) + suffixName + "." + imgType;
                var newImg = $('<img>').attr("src", newImgSrc).css('position', 'absolute');

                return newImg;
            }

            /**
             * 首次触发鼠标事件
             * Trigger first mouse event
             * 由于大图的宽高在首次进入容器时才能得到
             * Only get the width and height of big image on first mouse event
             * 因此一些依赖它的变量和常量的计算与其一起放到函数中
             * so some calculation of variables are put in the function which depend on them
             */
            function firstEnter() {
                $jzoom.append($jzoomLens).append($jzoomDiv);

                //计算镜头div的宽高比例
                //Calculate proportions of lens div
                var VolProportionX = $zoomImg.width() / $jzoom.width();
                var VolProportionY = $zoomImg.height() / $jzoom.height();

                $jzoomLens.css({
                    width: $jzoomDiv.width() / VolProportionX + "px",
                    height: $jzoomDiv.height() / VolProportionY + "px"
                });

                //计算镜头div的临界坐标
                //Calculate critical coordinates of lens div
                CriticalX = $jzoom.width() - $jzoomLens.outerWidth();
                CriticalY = $jzoom.height() - $jzoomLens.outerHeight();

                //计算大图的偏移比例
                //Calculate proportions of offsets of big image
                DistProportionX = ($zoomImg.width() - $jzoomDiv.width()) / CriticalX;
                DistProportionY = ($zoomImg.height() - $jzoomDiv.height()) / CriticalY;
            }

            /**
             * 计算距离
             * Calculate distance
             * @param  {Mumber} pageD     鼠标坐标 coordinates of mouse
             * @param  {Number} offsetD   容器偏移距离 offsets of container
             * @param  {Number} lensW     镜头div宽高 width or height of lens div
             * @param  {Number} criticalD 镜头div临界坐标 critical coordinates of lens div
             * @return {Number}           镜头div坐标 coordinates of lens div
             */
            function calcDistance(pageD, offsetD, lensW, criticalD) {
                var finalD,
                    distance = pageD - offsetD - lensW / 2;

                if (distance >= 0 && distance <= criticalD) {
                    finalD = distance;
                } else if (distance < 0) {
                    finalD = 0;
                } else {
                    finalD = criticalD;
                }

                return finalD;
            }

            return this;
        });
    };
})(jQuery);
