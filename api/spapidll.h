#ifndef spapidll_def
#define spapidll_def

typedef char            tinyint;
typedef unsigned char   u_tinyint;
typedef unsigned char   u_char;
typedef unsigned short  u_short;
typedef unsigned int    u_int;
typedef unsigned long   u_long;
typedef __int64          bigint;
typedef unsigned __int64 u_bigint;

typedef char STR4[4];
typedef char STR16[16];
typedef char STR40[40];

#define ORD_BUY         'B'			//买入//禦
#define ORD_SELL        'S'			//卖出//芥
#define STOP_LOSS       'L'
#define STOP_UP         'U'
#define STOP_DOWN       'D'

#define AO_PRC          ((long)0x7fffffff)	//竞价//膙基

#define ORD_LIMIT       0			//限价//基
#define ORD_AUCTION     2			//拍卖价//╃芥基
#define ORD_MARKET      6			//市场价//カ初基

#define COND_NONE       0			//一般//
#define COND_STOP       1
#define COND_SCHEDTIME  3
#define COND_OCOSTOP    4
#define COND_TRAILSTOP  6
#define COND_COMBO_OPEN     8
#define COND_COMBO_CLOSE    9
#define COND_STOP_PRC       11
#define COND_OCOSTOP_PRC    14
#define COND_TRAILSTOP_PRC  16

#define VLD_REST_OF_DAY   0
#define VLD_FILL_AND_KILL 1
#define VLD_FILL_OR_KILL  2
#define VLD_UNTIL_EXPIRE  3
#define VLD_SPEC_TIME     4

#define ACT_ADD_ORDER    1				// 增加订单// 糤璹虫
#define ACT_CHANGE_ORDER 2				// 修改订单// э璹虫
#define ACT_DELETE_ORDER 3				// 删除订单// 埃璹虫

/*订单状态*/
#define ORDSTAT_SENDING     0			// 发送中// 祇癳い
#define ORDSTAT_WORKING     1			// 工作中// い
#define ORDSTAT_INACTIVE    2			// 无效// 礚
#define ORDSTAT_PENDING     3			// 待定// ﹚
#define ORDSTAT_ADDING      4			// 增加中// 糤い
#define ORDSTAT_CHANGING    5			// 修改中// эい
#define ORDSTAT_DELETING    6			// 删除中// 埃い
#define ORDSTAT_INACTING    7			// 无效中// 礚い
#define ORDSTAT_PARTTRD_WRK 8			// 部分已成交并且还在工作中// 场だΘユ临い
#define ORDSTAT_TRADED      9			// 已成交// Θユ
#define ORDSTAT_DELETED     10			// 已删除// 埃
#define ORDSTAT_APPROVEWAIT 18			// 等待批准 //approve wait
#define ORDSTAT_TRADEDREP   20			// traded & reported
#define ORDSTAT_DELETEDREP  21			// deleted & reported
#define ORDSTAT_RESYNC_ABN  24			// resync abnormal
#define ORDSTAT_PARTTRD_DEL 28			// partial traded & deleted
#define ORDSTAT_PARTTRD_REP 29			// partial traded & reported (deleted)

#define OC_DEFAULT              '\0'
#define OC_OPEN                 'O'
#define OC_CLOSE                'C'
#define OC_MANDATORY_CLOSE      'M'

#define SP_MAX_DEPTH    20
#define SP_MAX_LAST     20

#define CTRLMASK_CTRL_LEVEL     1  //户口控制:级别
#define CTRLMASK_KICKOUT        2  //户口控制:踢走


typedef struct
{
    long Qty;                    //上日仓位 //ら 
    long DepQty;                 //存储仓位 //纗  
    long LongQty;                //今日长仓 //さら 
    long ShortQty;               //今日短仓 //さら祏 
    double TotalAmt;             //上日成交 //らΘユ 
    double DepTotalAmt;          //上日持仓总数(数量*价格) //ら羆计(计秖*基) 
    double LongTotalAmt;         //今日长仓总数(数量*价格) //さら羆计(计秖*基) 
    double ShortTotalAmt;        //今日短仓总数(数量*价格) //さら祏羆计(计秖*基) 
	double PLBaseCcy;            //盈亏(基本货币)
	double PL;                   //盈亏
    double ExchangeRate;         //汇率
    STR16 AccNo;                 //用户//ノめ 
    STR16 ProdCode;              //合约代码 //絏 
    char LongShort;              //上日持仓买卖方向 //ら禦芥よ 
    tinyint DecInPrice;          //小数点 //计翴 
} SPApiPos;

typedef struct
{
    double Price;              //价格 //基 
    double StopLevel;          //止损价格 //ゎ穕基 
    double UpLevel;            //上限水平 //キ 
    double UpPrice;            //上限价格 //基 
    double DownLevel;          //下限水平 //キ 
    double DownPrice;          //下限价格 //基 
    bigint ExtOrderNo;         //外部指示 //场ボ 
    long IntOrderNo;           //用户订单编号 //ノめ璹虫絪腹 
    long Qty;                  //剩下數量 //逞计秖
    long TradedQty;            //已成交数量 //Θユ计秖 
    long TotalQty;             //订单总数量//璹虫羆计秖 2012-12-20 xiaolin
    long ValidTime;            //有效时间 //Τ丁 
    long SchedTime;            //预订发送时间 //箇璹祇癳丁 
    long TimeStamp;            //服务器接收订单时间 //狝叭竟钡Μ璹虫丁 
    u_long OrderOptions;       //如果该合约支持收市后期货交易时段(T+1),可将此属性设为:1 //狦赣やΜカ戳砯ユ琿(T+1),盢妮┦砞:1 
    STR16 AccNo;               //用户帐号 //ノめ眀腹 
    STR16 ProdCode;            //合约代号 //腹 
    STR16 Initiator;           //下单用户 //虫ノめ  
    STR16 Ref;                 //参考 //把σ 
    STR16 Ref2;                //参考2 //把σ2 
    STR16 GatewayCode;         //网关 //呼闽 
    STR40 ClOrderId;           //用户自定订单参考//ノめ﹚璹虫把σ 2012-12-20 xiaolin
    char BuySell;              //买卖方向 //禦芥よ 
    char StopType;             //止损类型 //ゎ穕摸  
    char OpenClose;            //开平仓 //秨キ  
    tinyint CondType;          //订单条件类型 //璹虫兵ン摸 
    tinyint OrderType;         //订单类型 //璹虫摸  
    tinyint ValidType;         //订单有效类型 //璹虫Τ摸 
    tinyint Status;            //状态 //篈 
    tinyint DecInPrice;        //合约小数位 //计 
} SPApiOrder;

typedef struct
{
	long RecNo;		   //成交记录
    double Price;              //成交价格 //Θユ基
	double AvgPrice;           //成交均价
    bigint TradeNo;            //成交编号 //Θユ絪腹
    bigint ExtOrderNo;         //外部指示 //场ボ
    long IntOrderNo;           //用户订单编号 //ノめ璹虫絪腹
    long Qty;                  //成交数量 //Θユ计秖
    long TradeDate;            //成交日期 //Θユら戳
    long TradeTime;            //成交时间 //Θユ丁
    STR16 AccNo;               //用户 //ノめ
    STR16 ProdCode;            //合约代码 //絏
    STR16 Initiator;           //下单用户 //虫ノめ
    STR16 Ref;                 //参考 //把σ
    STR16 Ref2;                //参考2 //把σ2
    STR16 GatewayCode;         //网关 //呼闽
    STR40 ClOrderId;           //用户自定订单参考//ノめ﹚璹虫把σ 2012-12-20 xiaolin
    char BuySell;              //买卖方向 //禦芥よ
    char OpenClose;            //开平仓 //秨キ
    tinyint Status;            //状态 //篈
    tinyint DecInPrice;        //小数位 //计
} SPApiTrade;

#define REQMODE_UNSUBSCRIBE     0
#define REQMODE_SUBSCRIBE       1
#define REQMODE_SNAPSHOT        2


typedef struct
{
    double Margin;			//保证金//玂靡
    long ContractSize;		//合约价值//基
    STR16 MarketCode;		//交易所代码 //カ初絏
    STR16 InstCode;			//产品系列代码 //玻珇╰絏
    STR40 InstName;			//英文名称 //璣ゅ嘿
    STR40 InstName1;		//繁体名称 //羉砰嘿
    STR40 InstName2;		//简体名称 //虏砰嘿
    STR4 Ccy;				//产品系列的交易币种 //玻珇╰ユ刽贺
    char DecInPrice;		//产品系列的小数位 //玻珇╰计
    char InstType;			//产品系列的类型 //玻珇╰摸
} SPApiInstrument;

typedef struct
{
   STR16 ProdCode;			//产品代码 //玻珇絏
   char ProdType;			//产品类型 //玻珇摸
   STR40 ProdName;			//产品英文名称 //玻珇璣ゅ嘿
   STR16 Underlying;		//关联的期货合约//闽羛戳砯
   STR16 InstCode;			//产品系列名称 //玻珇╰嘿
   long ExpiryDate;			//产品到期时间 //玻珇戳丁
   char CallPut;			//期权方向认购与认沽 //戳舦よ粄潦籔粄猣
   long Strike;				//期权行使价//戳舦︽ㄏ基
   long LotSize;			//手数//も计
   STR40 ProdName1;			//产品繁体名称 //玻珇羉砰嘿
   STR40 ProdName2;			//产品简体名称 //玻珇虏砰嘿
   char OptStyle;			//期权的类型//戳舦摸
   long TickSize;			//产品价格最小变化位数//玻珇基程跑て计
}SPApiProduct;

#define SP_MAX_DEPTH    20
#define SP_MAX_LAST     20
typedef struct
{
    double Bid[SP_MAX_DEPTH];     //买入价 //禦基
    long BidQty[SP_MAX_DEPTH];    //买入量 //禦秖
    long BidTicket[SP_MAX_DEPTH]; //买指令数量 //禦计秖
    double Ask[SP_MAX_DEPTH];     //卖出价 //芥基
    long AskQty[SP_MAX_DEPTH];    //卖出量 //芥秖
    long AskTicket[SP_MAX_DEPTH]; //卖指令数量 //芥计秖
    double Last[SP_MAX_LAST];     //成交价 //Θユ基
    long LastQty[SP_MAX_LAST];    //成交数量 //Θユ计秖
    long LastTime[SP_MAX_LAST];   //成交时间 //Θユ丁
    double Equil;                 //平衡价 //キ颗基
    double Open;                  //开盘价 //秨絃基
    double High;                  //最高价 //程蔼基
    double Low;                   //最低价 //程基
    double Close;                 //收盘价 //Μ絃基
    long CloseDate;               //收市日期 //Μカら戳
    double TurnoverVol;           //总成交量 //羆Θユ秖
    double TurnoverAmt;           //总成交额 //羆Θユ肂
    long OpenInt;                 //未平仓 //ゼキ
    STR16 ProdCode;               //合约代码 //絏
    STR40 ProdName;               //合约名称 //嘿
    char DecInPrice;              //合约小数位 //计
} SPApiPrice;

typedef struct
{
    double Price;              //价格 //基
    long Qty;                  //成交量 //Θユ秖
    long TickerTime;           //时间 //丁
    long DealSrc;              //来源 //ㄓ方
    STR16 ProdCode;            //合约代码 //絏
    char DecInPrice;           //小数位 //计
} SPApiTicker;

typedef struct
{
	double NAV;               // 资产净值				//add xiaolin 2013-03-19
    double BuyingPower;       // 购买力					//add xiaolin 2013-03-19
    double CashBal;           // 现金结余				//add xiaolin 2013-03-19
	double MarginCall;        //追收金额
    double CommodityPL;       //商品盈亏
    double LockupAmt;         //冻结金额
    double CreditLimit;       //信贷限额 // 獺禪肂
    double MaxMargin;         //最高保证金 // 程蔼玂谍//modif xiaolin 2012-12-20 TradeLimit
    double MaxLoanLimit;      //最高借贷上限 // 程蔼禪
    double TradingLimit;      //信用交易額 // 獺ノユ肂
    double RawMargin;         //原始保證金 // ﹍玂靡
    double IMargin;           //基本保証金 //  膀セ玂谍
    double MMargin;           //維持保証金 // 蝴玂谍
    double TodayTrans;        //交易金額 // ユ肂
    double LoanLimit;         //證券可按總值 // 靡ㄩ羆
    double TotalFee;          //費用總額 //  禣ノ羆肂
    double LoanToMR;	      //借贷/可按值%
    double LoanToMV;	      //借贷/市值%    
    STR16 AccName;            //戶口名稱 //  め嘿
    STR4 BaseCcy;             //基本貨幣 // 膀セ砯刽
    STR16 MarginClass;        //保証金類別 // 玂谍摸
    STR16 TradeClass;         //交易類別 // ユ摸
    STR16 ClientId;           //客戶 // め
    STR16 AEId;               //經紀 //  竒
    char AccType;             //戶口類別 // め摸
    char CtrlLevel;           //控制級數 //  北计
    char Active;              //生效 //  ネ
    char MarginPeriod;        //時段 // 琿
} SPApiAccInfo;

typedef struct
{
    double CashBf;          //上日结余 //ら挡緇
    double TodayCash;       //今日存取 //さら
    double NotYetValue;     //未交收 //ゼユΜ
    double Unpresented;     //未兑现 //ゼ瞷
    double TodayOut;        //提取要求 //矗璶―
    STR4 Ccy;               //货币 //砯刽
} SPApiAccBal;

typedef struct
{
    STR4 Ccy;
    double Rate;
} SPApiCcyRate;


#define SPDLLCALL __stdcall
/*回调方法*/
typedef void (SPDLLCALL *LoginReplyAddr)(long ret_code, char *ret_msg);
typedef void (SPDLLCALL *LogoutReplyAddr)(long ret_code, char *ret_msg);
typedef void (SPDLLCALL *LoginStatusUpdateAddr)(long login_status);
typedef void (SPDLLCALL *LoginAccInfoAddr)(char *acc_no, int max_bal, int max_pos, int max_order);
typedef void (SPDLLCALL *ApiOrderRequestFailedAddr)(tinyint action, SPApiOrder *order, long err_code, char *err_msg);
typedef void (SPDLLCALL *ApiOrderReportAddr)(long rec_no, SPApiOrder *order);
typedef void (SPDLLCALL *ApiTradeReportAddr)(long rec_no, SPApiTrade *trade);
typedef void (SPDLLCALL *LoadTradeEndAddr)(char *acc_no);
typedef void (SPDLLCALL *LoadAETradeEndAddr)();
typedef void (SPDLLCALL *ApiPriceUpdateAddr)(SPApiPrice *price);
typedef void (SPDLLCALL *ApiTickerUpdateAddr)(SPApiTicker *ticker);
typedef void (SPDLLCALL *PServerLinkStatusUpdateAddr)(short host_id, long con_status);
typedef void (SPDLLCALL *ConnectionErrorAddr)(short host_id, long link_err);
typedef void (SPDLLCALL *InstrumentListReplyAddr)(bool is_ready, char *ret_msg);
typedef void (SPDLLCALL *PswChangeReplyAddr)(long ret_code, char *ret_msg);
typedef void (SPDLLCALL *ProductListByCodeReplyAddr)(char *inst_code, bool is_ready, char *ret_msg);
typedef void (SPDLLCALL *BusinessDateReplyAddr)(long business_date);

typedef void (SPDLLCALL *p_SPAPI_RegisterLoginReply)(LoginReplyAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterLogoutReply)(LogoutReplyAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterLoginStatusUpdate)(LoginStatusUpdateAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterLoginAccInfo)(LoginAccInfoAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterOrderRequestFailed)(ApiOrderRequestFailedAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterOrderReport)(ApiOrderReportAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterTradeReport)(ApiTradeReportAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterLoadTradeEnd)(LoadTradeEndAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterLoadAETradeEnd)(LoadAETradeEndAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterApiPriceUpdate)(ApiPriceUpdateAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterTickerUpdate)(ApiTickerUpdateAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterPServerLinkStatusUpdate)(PServerLinkStatusUpdateAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterConnectionErrorUpdate)(ConnectionErrorAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterInstrumentListReply)(InstrumentListReplyAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterPswChangeReply)(PswChangeReplyAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterProductListByCodeReply)(ProductListByCodeReplyAddr addr);
typedef void (SPDLLCALL *p_SPAPI_RegisterBusinessDateReply)(BusinessDateReplyAddr addr);

/*请求方法*/
typedef double (SPDLLCALL *p_SPAPI_GetDLLVersion)();
typedef int (SPDLLCALL *p_SPAPI_Initialize)();
typedef int (SPDLLCALL *p_SPAPI_Uninitialize)();
typedef void (SPDLLCALL *p_SPAPI_Poll)();
typedef void (SPDLLCALL *p_SPAPI_SetBackgroundPoll)(bool onoff);
typedef void (SPDLLCALL *p_SPAPI_SetLoginInfo)(char *host, int port, char *license, char *app_id, char *user_id, char *password);
typedef int (SPDLLCALL *p_SPAPI_Login)();
typedef int (SPDLLCALL *p_SPAPI_Logout)();
typedef int (SPDLLCALL *p_SPAPI_GetLoginStatus)(short host_id);

typedef int (SPDLLCALL *p_SPAPI_AddOrder)(SPApiOrder *order);
typedef int (SPDLLCALL *p_SPAPI_ChangeOrder)(SPApiOrder *order, double org_price, long org_qty);
typedef int (SPDLLCALL *p_SPAPI_DeleteOrder)(SPApiOrder *order);
typedef int (SPDLLCALL *p_SPAPI_ActivateOrder)(SPApiOrder *order);
typedef int (SPDLLCALL *p_SPAPI_InactivateOrder)(SPApiOrder *order);
typedef int (SPDLLCALL *p_SPAPI_GetOrderCount)();
typedef int (SPDLLCALL *p_SPAPI_GetOrder)(int idx, SPApiOrder *order);
typedef int (SPDLLCALL *p_SPAPI_GetOrderByOrderNo)(char *acc_no, long int_order_no, SPApiOrder *order);  
typedef int (SPDLLCALL *p_SPAPI_GetPosCount)();
typedef int (SPDLLCALL *p_SPAPI_GetPos)(int idx, SPApiPos *pos);
typedef int (SPDLLCALL *p_SPAPI_GetPosByProduct)(char *prod_code, SPApiPos *pos);
typedef int (SPDLLCALL *p_SPAPI_GetTradeCount)();
typedef int (SPDLLCALL *p_SPAPI_GetTrade)(int idx, SPApiTrade *trade);
typedef int (SPDLLCALL *p_SPAPI_GetTradeByTradeNo)(long int_order_no, bigint trade_no, SPApiTrade *trade);

typedef int (SPDLLCALL *p_SPAPI_SubscribePrice)(char *prod_code, int mode);
typedef int (SPDLLCALL *p_SPAPI_GetPriceCount)();
typedef int (SPDLLCALL *p_SPAPI_GetPrice)(int idx, SPApiPrice *price);
typedef int (SPDLLCALL *p_SPAPI_GetPriceByCode)(char *prod_code, SPApiPrice *price);

typedef int (SPDLLCALL *p_SPAPI_GetInstrumentCount)();
typedef int (SPDLLCALL *p_SPAPI_GetInstrument)(int idx, SPApiInstrument *inst);
typedef int (SPDLLCALL *p_SPAPI_GetInstrumentByCode)(char *inst_code, SPApiInstrument *inst);

typedef int (SPDLLCALL *p_SPAPI_GetProductCount)();
typedef int (SPDLLCALL *p_SPAPI_GetProduct)(int idx, SPApiProduct *prod);
typedef int (SPDLLCALL *p_SPAPI_GetProductByCode)(char *prod_code, SPApiProduct *prod);

typedef int (SPDLLCALL *p_SPAPI_SubscribeTicker)(char *prod_code, int mode);
typedef int (SPDLLCALL *p_SPAPI_GetAccInfo)(SPApiAccInfo *acc_info);
typedef int (SPDLLCALL *p_SPAPI_GetAccBalCount)();
typedef int (SPDLLCALL *p_SPAPI_GetAccBal)(int idx, SPApiAccBal *acc_bal);
typedef int (SPDLLCALL *p_SPAPI_GetAccBalByCurrency)(char *ccy, SPApiAccBal *acc_bal);
typedef int (SPDLLCALL *p_SPAPI_GetDllVersion)(char *dll_ver_no, char *dll_rel_no, char *dll_suffix);

typedef int (SPDLLCALL *p_SPAPI_LoadOrderReport)(char *acc_no);
typedef int (SPDLLCALL *p_SPAPI_LoadTradeReport)(char *acc_no);
typedef int (SPDLLCALL *p_SPAPI_LoadInstrumentList)();
typedef int (SPDLLCALL *p_SPAPI_LoadProductInfoListByCode)(char *inst_code);

typedef int (SPDLLCALL *p_SPAPI_ChangePassword)(char *old_psw, char *new_psw);
typedef int (SPDLLCALL *p_SPAPI_AccountLogin)(char *acc_no);
typedef int (SPDLLCALL *p_SPAPI_AccountLogout)(char *acc_no);
typedef int (SPDLLCALL *p_SPAPI_SetApiLogPath)(char *path);
typedef int (SPDLLCALL *p_SPAPI_SendAccControl)(char *acc_no, char ctrl_mask, char ctrl_level);
typedef int (SPDLLCALL *p_SPAPI_GetCcyRateCount)();
typedef int (SPDLLCALL *p_SPAPI_GetCcyRate)(int idx, SPApiCcyRate *ccy_rate);
typedef int (SPDLLCALL *p_SPAPI_GetCcyRateByCcy)(char *ccy, double &rate);

#endif

