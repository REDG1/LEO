import{p as J,W as Ee,g as X,e as W,f as t,i as re,X as he,Y as Le,Z as Be,$ as Ue,a0 as te,a1 as qe,c as L,a2 as Fe,a3 as He,a4 as _e,F as $,a5 as Ge,a6 as Ke,a7 as de,a8 as Je,a9 as Ve,aa as Xe,ab as We,ac as Qe,ad as Ye,d as Ze,t as K,h as ee,ae as Ce,af as De,ag as Te,ah as et,ai as ge,aj as tt,ak as lt,S as E,al as at,am as st,an as nt,s as ot,r as g,w as ue,ao as it,k as Ie,o as n,l as u,x as l,C as H,D as R,v as D,E as B,n as b,R as V,B as G,j as rt,q as F,y as x,z as ut,A as O,M as be,G as Y,H as se,N,I as ne,J as Z,ap as dt,_ as ct,aq as vt,ar as mt,P as oe,Q as ie,T as ft,U as yt}from"./assets/axios-CXuHkYsP.js";import{o as pt}from"./assets/VDataTable-CcyWH9Z-.js";const _t=J({...Ee({falseIcon:"$radioOff",trueIcon:"$radioOn"})},"VRadio"),ke=X()({name:"VRadio",props:_t(),setup(e,h){let{slots:r}=h;return W(()=>t(he,re(e,{class:["v-radio",e.class],style:e.style,type:"radio"}),r)),{}}}),gt=J({height:{type:[Number,String],default:"auto"},...Le(),...Be(Ue(),["multiple"]),trueIcon:{type:te,default:"$radioOn"},falseIcon:{type:te,default:"$radioOff"},type:{type:String,default:"radio"}},"VRadioGroup"),bt=X()({name:"VRadioGroup",inheritAttrs:!1,props:gt(),emits:{"update:modelValue":e=>!0},setup(e,h){let{attrs:r,slots:v}=h;const T=qe(),k=L(()=>e.id||`radio-group-${T}`),m=Fe(e,"modelValue");return W(()=>{const[d,y]=He(r),I=_e.filterProps(e),S=he.filterProps(e),p=v.label?v.label({label:e.label,props:{for:k.value}}):e.label;return t(_e,re({class:["v-radio-group",e.class],style:e.style},d,I,{modelValue:m.value,"onUpdate:modelValue":P=>m.value=P,id:k.value}),{...v,default:P=>{let{id:A,messagesId:Q,isDisabled:U,isReadonly:M}=P;return t($,null,[p&&t(Ge,{id:A.value},{default:()=>[p]}),t(Ke,re(S,{id:A.value,"aria-describedby":Q.value,defaultsTarget:"VRadio",trueIcon:e.trueIcon,falseIcon:e.falseIcon,type:e.type,disabled:U.value,readonly:M.value,"aria-labelledby":p?A.value:void 0,multiple:!1},y,{modelValue:m.value,"onUpdate:modelValue":z=>m.value=z}),v)])}})}),{}}}),kt=J({align:{type:String,default:"center",validator:e=>["center","start"].includes(e)},direction:{type:String,default:"vertical",validator:e=>["vertical","horizontal"].includes(e)},justify:{type:String,default:"auto",validator:e=>["auto","center"].includes(e)},side:{type:String,validator:e=>e==null||["start","end"].includes(e)},lineInset:{type:[String,Number],default:0},lineThickness:{type:[String,Number],default:2},lineColor:String,truncateLine:{type:String,validator:e=>["start","end","both"].includes(e)},...de(),...Je(),...Ve(),...Xe()},"VTimeline"),ht=X()({name:"VTimeline",props:kt(),setup(e,h){let{slots:r}=h;const{themeClasses:v}=We(e),{densityClasses:T}=Qe(e),{rtlClasses:k}=Ye();Ze({VTimelineDivider:{lineColor:K(e,"lineColor")},VTimelineItem:{density:K(e,"density"),lineInset:K(e,"lineInset")}});const m=L(()=>{const y=e.side?e.side:e.density!=="default"?"end":null;return y&&`v-timeline--side-${y}`}),d=L(()=>{const y=["v-timeline--truncate-line-start","v-timeline--truncate-line-end"];switch(e.truncateLine){case"both":return y;case"start":return y[0];case"end":return y[1];default:return null}});return W(()=>t(e.tag,{class:["v-timeline",`v-timeline--${e.direction}`,`v-timeline--align-${e.align}`,`v-timeline--justify-${e.justify}`,d.value,{"v-timeline--inset-line":!!e.lineInset},v.value,T.value,m.value,k.value,e.class],style:[{"--v-timeline-line-thickness":ee(e.lineThickness)},e.style]},r)),{}}}),Vt=J({dotColor:String,fillDot:Boolean,hideDot:Boolean,icon:te,iconColor:String,lineColor:String,...de(),...Ce(),...De(),...Te()},"VTimelineDivider"),Ct=X()({name:"VTimelineDivider",props:Vt(),setup(e,h){let{slots:r}=h;const{sizeClasses:v,sizeStyles:T}=et(e,"v-timeline-divider__dot"),{backgroundColorStyles:k,backgroundColorClasses:m}=ge(K(e,"dotColor")),{roundedClasses:d}=tt(e,"v-timeline-divider__dot"),{elevationClasses:y}=lt(e),{backgroundColorClasses:I,backgroundColorStyles:S}=ge(K(e,"lineColor"));return W(()=>t("div",{class:["v-timeline-divider",{"v-timeline-divider--fill-dot":e.fillDot},e.class],style:e.style},[t("div",{class:["v-timeline-divider__before",I.value],style:S.value},null),!e.hideDot&&t("div",{key:"dot",class:["v-timeline-divider__dot",y.value,d.value,v.value],style:T.value},[t("div",{class:["v-timeline-divider__inner-dot",m.value,d.value],style:k.value},[r.default?t(at,{key:"icon-defaults",disabled:!e.icon,defaults:{VIcon:{color:e.iconColor,icon:e.icon,size:e.size}}},r.default):t(E,{key:"icon",color:e.iconColor,icon:e.icon,size:e.size},null)])]),t("div",{class:["v-timeline-divider__after",I.value],style:S.value},null)])),{}}}),Dt=J({density:String,dotColor:String,fillDot:Boolean,hideDot:Boolean,hideOpposite:{type:Boolean,default:void 0},icon:te,iconColor:String,lineInset:[Number,String],...de(),...st(),...Te(),...Ce(),...De(),...Ve()},"VTimelineItem"),Tt=X()({name:"VTimelineItem",props:Dt(),setup(e,h){let{slots:r}=h;const{dimensionStyles:v}=nt(e),T=ot(0),k=g();return ue(k,m=>{var d;m&&(T.value=((d=m.$el.querySelector(".v-timeline-divider__dot"))==null?void 0:d.getBoundingClientRect().width)??0)},{flush:"post"}),W(()=>{var m,d;return t("div",{class:["v-timeline-item",{"v-timeline-item--fill-dot":e.fillDot},e.class],style:[{"--v-timeline-dot-size":ee(T.value),"--v-timeline-line-inset":e.lineInset?`calc(var(--v-timeline-dot-size) / 2 + ${ee(e.lineInset)})`:ee(0)},e.style]},[t("div",{class:"v-timeline-item__body",style:v.value},[(m=r.default)==null?void 0:m.call(r)]),t(Ct,{ref:k,hideDot:e.hideDot,icon:e.icon,iconColor:e.iconColor,size:e.size,elevation:e.elevation,dotColor:e.dotColor,fillDot:e.fillDot,rounded:e.rounded},{default:r.icon}),e.density!=="compact"&&t("div",{class:"v-timeline-item__opposite"},[!e.hideOpposite&&((d=r.opposite)==null?void 0:d.call(r))])])}),{}}}),It={name:"RecursiveItem",props:{data:{type:Object,required:!0}},methods:{isObject(e){return e!==null&&typeof e=="object"&&!Array.isArray(e)},isHtmlKey(e){return e.toLowerCase().includes("html")}}},St={key:0,class:""},$t={key:1},Pt={class:""},At=["innerHTML"],wt={key:3};function Ot(e,h,r,v,T,k){const m=Ie("RecursiveItem",!0);return n(),u("div",null,[t(G,null,{default:l(()=>[t(H,{"no-gutters":""},{default:l(()=>[(n(!0),u($,null,R(r.data,(d,y)=>(n(),D(B,{key:y,class:"pa-1 ma-1"},{default:l(()=>[b("strong",null,V(y)+":",1),k.isObject(d)?(n(),u("div",St,[t(m,{data:d},null,8,["data"])])):Array.isArray(d)?(n(),u("div",$t,[b("ul",Pt,[(n(!0),u($,null,R(d,(I,S)=>(n(),u("li",{key:S},V(I),1))),128))])])):k.isHtmlKey(y)?(n(),u("div",{key:2,innerHTML:d},null,8,At)):(n(),u("div",wt,V(d),1))]),_:2},1024))),128))]),_:1})]),_:1})])}const jt=it(It,[["render",Ot],["__scopeId","data-v-b51a4575"]]),xt={id:"start-page"},Rt={class:"text-h5"},Mt={key:0},zt={key:0},Nt={class:"ml-1"},Et={key:1},Lt={key:2},Bt={key:0},Ut={key:0},qt=["innerHTML"],Ft=b("h5",null,"Extracted Tables",-1),Ht={class:"bg-surface-light position-sticky top-0 pa-1 mt-1",style:{"z-index":"1"}},Gt={class:"pa-2"},Kt=b("div",null,[b("br"),b("br")],-1),Jt={__name:"cuLinksApp",props:["Links","csrf"],setup(e){const h=rt(),r=g(null),v=g("Dataset"),T=L(()=>(console.log(v.value),v.value==="Dataset"?p.value.data2show.filter(i=>i.provider==="OMERO").flatMap(i=>i.data).filter(i=>i.Type==="Image").map(i=>({Dataset:i.Dataset,ID:i.DatasetID})).filter((i,_,a)=>_===a.findIndex(f=>f.ID===i.ID)):p.value.data2show.filter(i=>i.provider==="OMERO").flatMap(i=>i.data).filter(i=>i.Type==="Image").map(i=>({Project:i.Project,ID:i.ProjectID})).filter((i,_,a)=>_===a.findIndex(f=>f.ID===i.ID)))),k=L(()=>v.value),m=L(()=>{const o=T.value.find(s=>s.ID===r.value);return v.value==="Dataset"?o?`Dataset Name: ${o.Dataset}, ID: ${o.ID}`:"Select a dataset to view details":o?`Project Name: ${o.Project}, ID: ${o.ID}`:"Select a project to view details"}),d=e,y=d.csrf,I=g(JSON.parse(d.Links.replaceAll(", 'children': []","").replace(/'/g,'"'))),S=g(Array(I.value.length).fill(!1)),p=g({visible:!1,id:null,ivalue:null,data2show:null}),P=g(!1),A=g(!1),Q=g(""),U=g(""),M=g(!1),z=g(!1),ce=g(""),ve=g(""),$e=L(()=>I.value.length===0);async function Pe(o,s,i,_){p.value.id=o,p.value.ivalue=i,await Oe(o,_),p.value.visible=!0}function Ae(o,s){M.value=!1,z.value=!1;const i=v.value,_=s.headers,a=s.items,f={Type:i,ID:o,table:{headers:_,items:a}};console.log("Sending the following JSON payload:",f),oe.post("/populateTable/",f,{headers:{"X-CSRFToken":y,"Content-Type":"application/json"}}).then(c=>{console.log("Data sent successfully:",c.data),ce.value="The table was successfully populate.",M.value=!0,z.value=!1,p.value.visible=!1}).catch(c=>{console.error("Error sending data:",c),ve.value="Failed to populate the table."+c,z.value=!0,M.value=!1})}function me(o){return o.toLowerCase().includes("html")}function we(o){return o!==null&&typeof o=="object"&&!Array.isArray(o)}async function Oe(o,s){S.value[s]=!0;const i={idlink:o};try{const _=await oe.get("/getMetadata/",{params:i});S.value[s]=!1,p.value.data2show=_.data.metadata}catch(_){S.value[s]=!1,p.value.data2show=[{provider:"Error in the connection with the data providers.",data:_}]}}function je(o){const s={data:o};oe.post("/removeLinks/",s,{headers:{"X-CSRFToken":y,"Content-Type":"application/json"}}).then(function(i){i.data.deleted==="True"?(I.value=I.value.filter(a=>a.id!==o),Q.value="The item has been removed successfully.",P.value=!0,A.value=!1,ie(()=>{h("#start-page",{offset:0})})):(U.value="The item could not be removed due to an error.",A.value=!0,P.value=!1,ie(()=>{h("#start-page",{offset:0})}))}).catch(i=>{U.value="The item could not be removed due to an error.",A.value=!0,P.value=!1,ie(()=>{h("#start-page",{offset:0})})})}const le=g({Dataset:"$mdiDatabase",Experiment:"$mdiFlask",Image:"$mdiImage",Project:"$mdiFolderMultipleImage",Spectra:"$mdiWaveform",other:"$mdiFile"}),j=g({visible:!1,tables:[]});ue(()=>j.value.visible,o=>{o||(r.value=null)}),ue(v,o=>{r.value=null});async function xe(o){j.value.tables=Re(o),j.value.visible=!0}function Re(o){const i=new DOMParser().parseFromString(o,"text/html"),_=[];return i.querySelectorAll("table").forEach(f=>{const c=Array.from(f.querySelectorAll("tr")),w=Array.from(c[0].querySelectorAll("td, th")).map(q=>({title:q.innerText.trim(),value:q.innerText.trim()})),C=c.slice(1).map(q=>{const Me=Array.from(q.querySelectorAll("td")),fe={};return Me.forEach((ze,ye)=>{var pe;const Ne=((pe=w[ye])==null?void 0:pe.value)||`column_${ye}`;fe[Ne]=ze.innerText.trim()}),fe});_.push({headers:w,items:C})}),_}return(o,s)=>{const i=Ie("v-treeview"),_=ct;return n(),u($,null,[b("div",xt,[t(F,{modelValue:P.value,"onUpdate:modelValue":s[0]||(s[0]=a=>P.value=a),text:Q.value,type:"success",density:"compact",closable:""},null,8,["modelValue","text"]),t(F,{modelValue:A.value,"onUpdate:modelValue":s[1]||(s[1]=a=>A.value=a),text:U.value,type:"error",variant:"tonal",border:"top",density:"compact",closable:""},null,8,["modelValue","text"]),$e.value?(n(),D(F,{key:0,color:"cyan-darken-4",density:"compact",closable:""},{default:l(()=>[O(' Currently there is no link, please go to the "Links creation" tab to add a new link ')]),_:1})):x("",!0)]),t(ut,null,{default:l(()=>[t(G,null,{default:l(()=>[t(H,{justify:"center"},{default:l(()=>[(n(!0),u($,null,R(I.value,(a,f)=>(n(),D(B,{md:"3",key:f,cols:"auto"},{default:l(()=>[t(Y,null,{default:l(()=>[t(se,{color:"cyan-darken-4",flat:""},{default:l(()=>[t(ne,null,{default:l(()=>[b("h5",null,"Link "+V(f+1),1)]),_:2},1024),t(N,{onClick:c=>Pe(a.id,a.title,f+1,f),class:"ma-2",variant:"tonal",icon:"$mdiEye",loading:S.value[f]},null,8,["onClick","loading"]),t(N,{class:"ma-2",variant:"tonal",icon:"$mdiDelete",onClick:c=>je(a.id)},null,8,["onClick"])]),_:2},1024),t(Z,null,{default:l(()=>[t(i,{items:a.data,"item-value":"id","open-all":""},{prepend:l(({item:c,open:ae})=>[c.elemnt_type?(n(),D(E,{key:1,color:"teal-darken-2"},{default:l(()=>[O(V(le.value[c.elemnt_type]),1)]),_:2},1024)):(n(),D(E,{key:0,icon:"$mdiApplicationOutline",color:"teal-darken-2"}))]),_:2},1032,["items"])]),_:2},1024)]),_:2},1024)]),_:2},1024))),128))]),_:1}),t(be,{modelValue:p.value.visible,"onUpdate:modelValue":s[3]||(s[3]=a=>p.value.visible=a),transition:"dialog-bottom-transition"},{default:l(()=>[t(Y,{class:"overflow-auto"},{default:l(()=>[t(se,{color:"cyan-darken-4"},{append:l(()=>[t(N,{icon:"$close",variant:"text",onClick:s[2]||(s[2]=a=>p.value.visible=!1)})]),default:l(()=>[t(ne,null,{default:l(()=>[b("h5",null,"Link - "+V(p.value.ivalue),1)]),_:1})]),_:1}),t(Z,{class:"bg-surface-bright"},{default:l(()=>[t(ht,{align:"start",side:"end"},{default:l(()=>[(n(!0),u($,null,R(p.value.data2show,(a,f)=>(n(),D(Tt,{key:f,size:"large","dot-color":"teal-darken-2","fill-dot":""},{icon:l(()=>[a.elemnt_type?(n(),D(E,{key:1,color:"teal-darken-2"},{default:l(()=>[O(V(le.value[a.elemnt_type]),1)]),_:2},1024)):(n(),D(E,{key:0,icon:"$mdiApplicationOutline"}))]),opposite:l(()=>[b("span",Rt,V(a.provider),1)]),default:l(()=>[(n(!0),u($,null,R(a.data,(c,ae)=>(n(),D(Y,{class:"elevation-2 mb-4 overflow-auto",key:ae},{default:l(()=>[t(vt,{class:"mb-0 pb-0"},{default:l(()=>[c.Type?(n(),D(E,{key:1,icon:le.value[c.Type],color:"teal-darken-2",class:"mr-2",size:"small"},null,8,["icon"])):(n(),D(E,{key:0,icon:"$mdiApplicationOutline",class:"mr-2",size:"small"})),O(" "+V(c.Name),1)]),_:2},1024),c.Type?(n(),D(mt,{key:0,class:"mt-n1 mb-2"},{default:l(()=>[O(V(c.Type),1)]),_:2},1024)):x("",!0),t(Z,{class:"bg-surface-light"},{default:l(()=>[t(G,null,{default:l(()=>[t(H,null,{default:l(()=>[o.key!=="Type"&&o.key!=="Name"?(n(!0),u($,{key:0},R(c,(w,C)=>(n(),u("div",{key:C},[C!=="Type"&&C!=="Name"?(n(),u("div",Mt,[t(B,{md:"12",class:"pa-1 ma-1",cols:"auto"},{default:l(()=>[we(w)?(n(),u("div",zt,[b("strong",null,V(C)+":",1),b("div",Nt,[t(jt,{data:w},null,8,["data"])])])):me(C)?(n(),u("div",Et)):(n(),u("div",Lt,[b("strong",null,V(C)+" :",1),O(" "+V(w),1)]))]),_:2},1024)])):x("",!0)]))),128)):x("",!0)]),_:2},1024),t(H,null,{default:l(()=>[o.key!=="Type"&&o.key!=="Name"?(n(!0),u($,{key:0},R(c,(w,C)=>(n(),u("div",{key:C},[C!=="Type"&&C!=="Name"?(n(),u("div",Bt,[me(C)?(n(),u("div",Ut,[t(B,{md:"12",class:"pa-1 ma-1"},{default:l(()=>[a.provider!=="OMERO"?(n(),D(N,{key:0,color:"teal","prepend-icon":"$mdiPlusCircle",onClick:q=>xe(w),class:"ma-2 pa-2"},{default:l(()=>[O(" Additional actions ")]),_:2},1032,["onClick"])):x("",!0)]),_:2},1024),b("div",{innerHTML:w},null,8,qt)])):x("",!0)])):x("",!0)]))),128)):x("",!0)]),_:2},1024)]),_:2},1024)]),_:2},1024)]),_:2},1024))),128))]),_:2},1024))),128))]),_:1})]),_:1})]),_:1})]),_:1},8,["modelValue"]),t(be,{modelValue:j.value.visible,"onUpdate:modelValue":s[10]||(s[10]=a=>j.value.visible=a),transition:"dialog-bottom-transition"},{default:l(()=>[t(Y,{class:"overflow-auto"},{default:l(()=>[t(se,{color:"cyan-darken-4"},{default:l(()=>[t(ne,null,{default:l(()=>[Ft]),_:1}),t(N,{icon:"$close",variant:"text",onClick:s[4]||(s[4]=a=>j.value.visible=!1)})]),_:1}),t(Z,{class:"bg-surface-bright"},{default:l(()=>[t(G,{class:""},{default:l(()=>[b("div",Ht,[t(G,null,{default:l(()=>[t(H,{dense:""},{default:l(()=>[t(B,{md:"2"},{default:l(()=>[t(bt,{modelValue:v.value,"onUpdate:modelValue":s[5]||(s[5]=a=>v.value=a),inline:"",label:"Target Object"},{default:l(()=>[t(ke,{label:"Dataset",value:"Dataset"}),t(ke,{label:"Project",value:"Project"})]),_:1},8,["modelValue"])]),_:1}),t(B,{cols:"12",md:"6"},{default:l(()=>[t(dt,{modelValue:r.value,"onUpdate:modelValue":s[6]||(s[6]=a=>r.value=a),hint:m.value,items:T.value,"item-title":k.value,"item-value":"ID",label:`Select ${k.value} for Metadata Population`,"persistent-hint":""},null,8,["modelValue","hint","items","item-title","label"])]),_:1})]),_:1})]),_:1}),b("div",Gt,[t(F,{modelValue:M.value,"onUpdate:modelValue":s[7]||(s[7]=a=>M.value=a),text:ce.value,type:"success",density:"compact",closable:""},null,8,["modelValue","text"]),t(F,{modelValue:z.value,"onUpdate:modelValue":s[8]||(s[8]=a=>z.value=a),text:ve.value,type:"error",variant:"tonal",border:"top",density:"compact",closable:""},null,8,["modelValue","text"])])]),(n(!0),u($,null,R(j.value.tables,(a,f)=>(n(),u("div",{key:f,class:"mb-4"},[t(N,{rounded:"xl",color:"teal",variant:"tonal",onClick:c=>Ae(r.value,a),"prepend-icon":"$mdiPlusCircle",class:"ma-2 pa-2",disabled:!r.value},{default:l(()=>[O(" Use this table to populate "+V(m.value),1)]),_:2},1032,["onClick","disabled"]),t(pt,{class:"custom-header",headers:a.headers,items:a.items,"items-per-page":5},{"no-data":l(()=>[t(N,{color:"primary",onClick:s[9]||(s[9]=c=>j.value.visible=!1)},{default:l(()=>[O(" Close ")]),_:1})]),_:2},1032,["headers","items"])]))),128))]),_:1})]),_:1})]),_:1})]),_:1},8,["modelValue"])]),_:1}),Kt,t(_)]),_:1})],64)}}},Xt=document.getElementById("Links").getAttribute("value")||"{}",Wt=document.getElementsByName("csrfmiddlewaretoken")[0].getAttribute("value")||"",Se=ft(Jt,{Links:Xt,csrf:Wt});yt(Se);Se.mount("#app");
