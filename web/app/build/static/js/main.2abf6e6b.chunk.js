(this.webpackJsonptemp=this.webpackJsonptemp||[]).push([[0],{48:function(e,t,c){},62:function(e,t,c){"use strict";c.r(t);c(48);var n,s,i=c(0),a=c.n(i),r=c(37),l=c.n(r),d=c(4),j=c(12),o=c(9),b=c(16),x=c(17),m=c(21),h=c(20),O=c(13),v=c(14),g=c(1),u=v.a.div(n||(n=Object(O.a)(["\n  overflow: auto;\n  min-height: 75vh;\n  margin: 25px;\n"]))),p=function(e){Object(m.a)(c,e);var t=Object(h.a)(c);function c(){return Object(b.a)(this,c),t.apply(this,arguments)}return Object(x.a)(c,[{key:"render",value:function(){return Object(g.jsxs)("div",{className:"col-xl-12 col-lg-12",children:[Object(g.jsx)("div",{className:" card-header py-3 d-flex flex-row align-items-center bg-white justify-content-between ",children:Object(g.jsx)("h6",{className:"m-0 text-dark",children:"Load Balance"})}),Object(g.jsx)(u,{children:Object(g.jsx)("div",{className:"chart-area",children:this.props.children})})]})}}]),c}(a.a.Component),f=c(5),N=c(25),y=c.n(N),k=c(41),w=c.n(k),S=c(42);c.n(S)()(y.a);var C,E,T=v.a.div(s||(s=Object(O.a)([""]))),P={chart:{type:"column",zoomType:"xy"},title:{text:"PET Timings"},credits:{enabled:!1},xAxis:{categories:[1,2,3],title:{text:"PET Number"}},yAxis:{min:0,allowDecimals:!0,title:{text:"Time (s)"}},legend:{reversed:!0,itemStyle:{fontSize:"12pt"}},plotOptions:{series:{stacking:"normal",events:{click:function(e){alert("you clicked series: "+this.name)}}}},series:[1,2,3,4],navigation:{menuStyle:{background:"#E0E0E0"}}},A=function(e){Object(m.a)(c,e);var t=Object(h.a)(c);function c(e){var n;return Object(b.a)(this,c),(n=t.call(this,e)).config=Object(f.a)(Object(f.a)({},P),n.props.config),console.log(n.props.config),n}return Object(x.a)(c,[{key:"render",value:function(){return Object(g.jsx)(T,{children:Object(g.jsx)(w.a,{highcharts:y.a,options:this.config})})}}]),c}(a.a.Component),I=c(47),L=c(15),M=c(45),F=c(22);v.a.div(C||(C=Object(O.a)(["\n  text-decoration: none;\n  font-size: 1.1rem;\n  padding: 1.5rem 1rem;\n  text-align: center;\n  letter-spacing: 0.05rem;\n"]))),v.a.div(E||(E=Object(O.a)(["\n  width: 10px;\n"])));function z(){var e=Object(i.useState)(!0),t=Object(o.a)(e,2),c=t[0],n=t[1];return Object(g.jsxs)(a.a.Fragment,{children:[Object(g.jsx)("br",{}),Object(g.jsx)(I.a,{className:"flex-column",bg:"gradient-dark",children:Object(g.jsxs)("ul",{"data-toggle":"collapse",className:"navbar-nav bg-gradient-dark sidebar sidebar-dark accordion ".concat(c?"":"toggled"),id:"accordionSidebar",children:[Object(g.jsx)("div",{className:"sidebar-brand d-flex align-items-center justify-content-center",children:Object(g.jsxs)("div",{className:"sidebar-brand-text",children:["ESMF Profiler"," ",Object(g.jsx)("div",{children:Object(g.jsx)("img",{src:"https://img.shields.io/badge/version-0.1.0-success"})})]})}),Object(g.jsx)("hr",{className:"sidebar-divider my-10"}),Object(g.jsx)("div",{className:"sidebar-heading",children:"Application Info"}),Object(g.jsx)("li",{className:"nav-item",children:Object(g.jsxs)(j.b,{className:"nav-link text-muted",to:"/",children:[Object(g.jsx)(L.a,{icon:F.a}),Object(g.jsx)("span",{children:" Component Configuration"})]})}),Object(g.jsx)("hr",{className:"sidebar-divider"}),Object(g.jsx)("div",{className:"sidebar-heading",children:"Timing"}),Object(g.jsx)("li",{className:"nav-item",children:Object(g.jsxs)(j.b,{className:"nav-link text-muted",to:"/",children:[Object(g.jsx)(L.a,{icon:F.c}),Object(g.jsx)("span",{children:" Timing Summary"})]})}),Object(g.jsx)("li",{className:"nav-item",children:Object(g.jsxs)(j.b,{className:"nav-link",to:"/",children:[Object(g.jsx)(L.a,{icon:F.b}),Object(g.jsx)("span",{children:" Load Balance"})]})}),Object(g.jsx)("li",{className:"nav-item",children:Object(g.jsxs)(j.b,{className:"nav-link text-muted",to:"/",children:[Object(g.jsx)(L.a,{icon:F.e}),Object(g.jsx)("span",{children:" MPI Profile"})]})}),Object(g.jsx)("hr",{className:"sidebar-divider"}),Object(g.jsx)("div",{className:"sidebar-heading",children:" Memory"}),Object(g.jsx)("li",{className:"nav-item",children:Object(g.jsxs)(j.b,{className:"nav-link text-muted",to:"/",children:[Object(g.jsx)(L.a,{icon:M.a}),Object(g.jsx)("span",{children:" Memory Profile"})]})}),Object(g.jsx)("div",{className:"sidebar-heading",children:"I/O"}),Object(g.jsx)("li",{className:"nav-item",children:Object(g.jsxs)(j.b,{className:"nav-link text-muted",to:"/",children:[Object(g.jsx)(L.a,{icon:F.d}),Object(g.jsx)("span",{children:" NetCDF Profile"})]})}),Object(g.jsx)("hr",{className:"sidebar-divider d-none d-md-block"}),Object(g.jsx)("div",{class:"text-center d-none d-md-inline",children:Object(g.jsx)("button",{class:"rounded-circle border-0",id:"sidebarToggle",onClick:function(){c||document.body.classList.add("sidebar-toggled"),document.body.classList.remove("sidebar-toggled"),n(!c),console.log("CLICK")}})})]})})]})}a.a.Component;var B=c(27);var D=function(){var e=Object(i.useState)(),t=Object(o.a)(e,2),c=t[0],n=t[1];return fetch("../data/load_balance2.json").then((function(e){return e.json()})).then((function(e){var t="/ROOT",c=e[t];n({title:{text:t},xAxis:{categories:c.xvals},series:c.yvals})})).catch((function(e){console.log(e,"Error loading JSON data")})),Object(g.jsxs)("div",{className:"App",children:[Object(g.jsx)(B.a,{title:Date.now().toString()}),Object(g.jsxs)("div",{id:"wrapper",children:[Object(g.jsx)(z,{}),Object(g.jsx)("div",{id:"content-wrapper",className:"d-flex flex-column",children:Object(g.jsx)("div",{id:"content",children:Object(g.jsxs)("div",{className:"container-fluid bg-white",children:[Object(g.jsx)("div",{className:"d-sm-flex align-items-center justify-content-between mb-4",children:Object(g.jsx)("h1",{className:"h3 mb-0 text-gray-800"})}),Object(g.jsx)("div",{className:"row",children:c?Object(g.jsx)(p,{children:Object(g.jsx)(A,{config:c})}):Object(g.jsx)("div",{children:c})})]})})})]})]})};function J(){return Object(g.jsx)("div",{children:Object(g.jsxs)(B.b,{children:[Object(g.jsxs)(B.a,{children:[Object(g.jsx)("title",{children:"ESMF Profiler"}),Object(g.jsx)("link",{rel:"canonical",href:"https://earthsystemmodeling.org/"})]}),Object(g.jsx)(d.c,{children:Object(g.jsx)(d.a,{path:"/",children:Object(g.jsx)(D,{})})})]})})}l.a.render(Object(g.jsx)(j.a,{children:Object(g.jsx)(J,{})}),document.getElementById("root"))}},[[62,1,2]]]);
//# sourceMappingURL=main.2abf6e6b.chunk.js.map