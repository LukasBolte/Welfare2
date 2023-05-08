var tdList={};
var selectedCutoff;
var cutoffHistory=[];

var leftDiv;
var rightDiv;
var offsetsY={};
var countTD={};
var countTDtotal=0;
var minY;
var maxY;
var tdHeight;

var drawChoices = function(base){
    var table=document.createElement("table");
    table.className="table table-hover";
    base.appendChild(table);
    //add header
    thead=document.createElement("thead");
    table.appendChild(thead);
    var trHead=document.createElement("tr");
    thead.appendChild(trHead);
    //now column headers
    var thHead=document.createElement("th");
    thHead.className="text-center";
    thHead.setAttribute("scope","col");
    trHead.appendChild(thHead);
    var text=document.createTextNode(charityHeader);
    thHead.appendChild(text);
    var thHead=document.createElement("th");
    thHead.setAttribute("scope","col");
    thHead.style.width="35%";
    trHead.appendChild(thHead);
    var thHead=document.createElement("th");
    thHead.setAttribute("scope","col");
    thHead.style.width="20%";
    trHead.appendChild(thHead);
    var text=document.createTextNode(selfHeader);
    thHead.appendChild(text);
    thHead.className="text-center";
    thHead.style.width="35%";
    //create body
    var tbody=document.createElement("tbody");
    tbody.addEventListener("mouseleave", unhighlight.bind(this));
    table.appendChild(tbody);
    var counter=0;
    for(var i=0;i<=charityPayout;i=i+stepSize){
        tr=document.createElement("tr");
        tdList[i]=[];
        tbody.appendChild(tr);
        //left choice
        td=document.createElement("td");
        td.className="text-center";
        var text=document.createTextNode(charityPayout+" CENTS");
        td.appendChild(text);
        td.setAttribute("cutoff","left:"+i);
        tr.appendChild(td);
        tdList[i].push(td);
        offsetsY[i]=td.offsetTop;
        countTD[i]=counter;
        if (i==0){
            minY=td.offsetTop;
            tdHeight=window.getComputedStyle(td).height;
        }
        td.setAttribute("data-toggle","tooltip");
        td.setAttribute("data-placement","bottom");
        td.setAttribute("title","Click here so that left option is chosen when bonus payment is less or equal to "+i+" and otherwise right option is chosen.");
        td.addEventListener("click", selectCutoff.bind(this));
        td.addEventListener("mouseenter", highlightSelection.bind(this));
        //middle OR
        td=document.createElement("td");
        td.className="text-center";
        text=document.createTextNode("OR");
        td.setAttribute("cutoff","middle:"+i);
        td.appendChild(text);
        tr.appendChild(td);
        td.setAttribute("data-toggle","tooltip");
        td.setAttribute("data-placement","bottom");
        td.setAttribute("title","Move the mouse to the left or right choice and click to select.");
        td.addEventListener("mouseenter", highlightSelection.bind(this));
        //right choice
        td=document.createElement("td");
        td.className="text-center";
        text=document.createTextNode(i+" CENTS");
        td.appendChild(text);
        td.setAttribute("cutoff","right:"+i);
        tr.appendChild(td);        
        tdList[i].push(td);
        td.setAttribute("data-toggle","tooltip");
        td.setAttribute("data-placement","bottom");
        td.setAttribute("title","Click here so that right option is chosen when bonus payment is greater or equal to "+i+" and otherwise left option is chosen.");
        td.addEventListener("click", selectCutoff.bind(this));
        td.addEventListener("mouseenter", highlightSelection.bind(this));
        counter++;
    }
    countTDtotal=counter;
    maxY=td.offsetTop;
}

var drawExplainer=function(on_left,ymin,ymax,text){
    var base=rightDiv;
    if (on_left){
        base=leftDiv;
    }
    $(base).empty();
    var div=document.createElement("div");
    base.appendChild(div);
    div.innerHTML=text;
    div.style.width=window.getComputedStyle(base).width;
    var h=parseFloat(window.getComputedStyle(div).height);
    div.style.position="absolute";
    div.style.top=(-h/2+(ymin+ymax)/2)+"px";
}

var formatExplainer = function(rows,leftright){
    if (rows==1){
        return "If this row is selected for payment you are choosing the "+leftright+" option."
    }
    else{  
        return "If one of these "+rows+" rows is selected for payment you are choosing the "+leftright+" option."
    }
}

var highlight = function(cutoff,color,drawExplainers=false){
    var choiceFrags=cutoff.split(':');
    var cutoffNum=parseFloat(choiceFrags[1]);
    for(var c in tdList){
        var cf=parseFloat(c);
        $(tdList[c][0]).removeClass("orange");
        $(tdList[c][0]).removeClass("darkorange");
        $(tdList[c][1]).removeClass("orange");
        $(tdList[c][1]).removeClass("darkorange");
        if (cf<cutoffNum){
            $(tdList[c][0]).addClass(color);
        }
        if (cf>cutoffNum){
            $(tdList[c][1]).addClass(color);
        }
        if (cf==cutoffNum){
            switch(choiceFrags[0]){
                case "left":
                    $(tdList[c][0]).addClass(color);
                    if (drawExplainers){
                        var y1=parseFloat(minY);
                        var y2=parseFloat(offsetsY[c])+parseFloat(tdHeight);
                        if (y1<y2){
                            drawExplainer(true,y1,y2,formatExplainer(parseFloat(countTD[c])+1,"left"));
                        }
                        else{
                            leftDiv.innerHTML="&nbsp;";
                        }
                        y1=parseFloat(offsetsY[c])+parseFloat(tdHeight);
                        y2=parseFloat(maxY)+parseFloat(tdHeight);
                        if (y1<y2){
                            drawExplainer(false,y1,y2,formatExplainer(parseFloat(countTDtotal)-parseFloat(countTD[c])-1,"right"));
                        }
                        else{
                            rightDiv.innerHTML="&nbsp;";
                        }
                    }
                    break;
                case "middle":
                    break;
                case "right":
                    $(tdList[c][1]).addClass(color);
                    if (drawExplainers){
                        var y1=parseFloat(minY);
                        var y2=parseFloat(offsetsY[c]);
                        if (y1<y2){
                            drawExplainer(true,y1,y2,formatExplainer(parseFloat(countTD[c]),"left"));
                        }
                        else{
                            leftDiv.innerHTML="&nbsp;";
                        }
                        y1=parseFloat(offsetsY[c]);
                        y2=parseFloat(maxY)+parseFloat(tdHeight);
                        if (y1<y2){
                            drawExplainer(false,y1,y2,formatExplainer(parseFloat(countTDtotal)-parseFloat(countTD[c]),"right"));
                        }
                        else{
                            rightDiv.innerHTML="&nbsp;";
                        }
                    }
                    break;
            }
        }
    }    
}

var unhighlight = function(){
    if (this.selectedCutoff){
        return;
    }
    for(var c in tdList){
        $(tdList[c][0]).removeClass("orange");
        $(tdList[c][1]).removeClass("orange");
        $(tdList[c][0]).removeClass("darkorange");
        $(tdList[c][1]).removeClass("darkorange");
    }
}

var showNext=function(){
    var nextButton=document.getElementById("id_next_button");
    if (nextButton){
        nextButton.style.display="";
    }
}

var selectCutoff = function(e){
    if (selectedCutoff){
        cutoffHistory.push(selectedCutoff);
    }
    var cutoff=e.target.getAttribute("cutoff");
    selectedCutoff=cutoff;
    highlight(cutoff,"darkorange",true);
    //save data in hidden field
    document.getElementById(varname).value=JSON.stringify({"history":cutoffHistory,"cutoff":selectedCutoff});     
    console.log(document.getElementById(varname).value);  
    //make the oTree next button appear if present
    setTimeout(showNext,2000);
}

var highlightSelection = function(e){
    e.target.style.cursor = "pointer";
    if (selectedCutoff){
        return;
    }
    var cutoff=e.target.getAttribute("cutoff");
    highlight(cutoff,"orange");
}


var drawAltruismGame=function(){
    var hiddenDiv = document.getElementById("hidden_fields_altruism_game");
    var hiddenField=document.createElement("input");
    hiddenDiv.appendChild(hiddenField);
    hiddenField.setAttribute("type","hidden");
    hiddenField.setAttribute("name",varname);
    hiddenField.setAttribute("id",varname); 
    //draw game  
    var container=document.createElement("div");
    container.className="container";
    document.getElementById("altruism_game").appendChild(container);
    var row=document.createElement("div");
    row.className="row";
    container.appendChild(row);
    leftDiv=document.createElement("div");
    leftDiv.className="col-2";
    leftDiv.innerHTML="&nbsp;";
    row.appendChild(leftDiv);
    var midDiv=document.createElement("div");
    midDiv.className="col-8";
    row.appendChild(midDiv);
    rightDiv=document.createElement("div");
    rightDiv.className="col-2";
    rightDiv.innerHTML="&nbsp;";
    row.appendChild(rightDiv);
    drawChoices(midDiv);
}

drawAltruismGame();