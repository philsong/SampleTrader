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

#define ORD_BUY         'B'			//����//�R�J
#define ORD_SELL        'S'			//����//��X
#define STOP_LOSS       'L'
#define STOP_UP         'U'
#define STOP_DOWN       'D'

#define AO_PRC          ((long)0x7fffffff)	//����//�v��

#define ORD_LIMIT       0			//�޼�//����
#define ORD_AUCTION     2			//������//����
#define ORD_MARKET      6			//�г���//������

#define COND_NONE       0			//һ��//�@��
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

#define ACT_ADD_ORDER    1				// ���Ӷ���// �W�[�q��
#define ACT_CHANGE_ORDER 2				// �޸Ķ���// �ק�q��
#define ACT_DELETE_ORDER 3				// ɾ������// �R���q��

/*����״̬*/
#define ORDSTAT_SENDING     0			// ������// �o�e��
#define ORDSTAT_WORKING     1			// ������// �u�@��
#define ORDSTAT_INACTIVE    2			// ��Ч// �L��
#define ORDSTAT_PENDING     3			// ����// �ݩw
#define ORDSTAT_ADDING      4			// ������// �W�[��
#define ORDSTAT_CHANGING    5			// �޸���// �ק襤
#define ORDSTAT_DELETING    6			// ɾ����// �R����
#define ORDSTAT_INACTING    7			// ��Ч��// �L�Ĥ�
#define ORDSTAT_PARTTRD_WRK 8			// �����ѳɽ����һ��ڹ�����// �����w����åB�٦b�u�@��
#define ORDSTAT_TRADED      9			// �ѳɽ�// �w����
#define ORDSTAT_DELETED     10			// ��ɾ��// �w�R��
#define ORDSTAT_APPROVEWAIT 18			// �ȴ���׼ //approve wait
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

#define CTRLMASK_CTRL_LEVEL     1  //���ڿ���:����
#define CTRLMASK_KICKOUT        2  //���ڿ���:����


typedef struct
{
    long Qty;                    //���ղ�λ //�W��ܦ� 
    long DepQty;                 //�洢��λ //�s�x�ܦ�  
    long LongQty;                //���ճ��� //������� 
    long ShortQty;               //���ն̲� //����u�� 
    double TotalAmt;             //���ճɽ� //�W�馨�� 
    double DepTotalAmt;          //���ճֲ�����(����*�۸�) //�W������`��(�ƶq*����) 
    double LongTotalAmt;         //���ճ�������(����*�۸�) //��������`��(�ƶq*����) 
    double ShortTotalAmt;        //���ն̲�����(����*�۸�) //����u���`��(�ƶq*����) 
	double PLBaseCcy;            //ӯ��(��������)
	double PL;                   //ӯ��
    double ExchangeRate;         //����
    STR16 AccNo;                 //�û�//�Τ� 
    STR16 ProdCode;              //��Լ���� //�X���N�X 
    char LongShort;              //���ճֲ��������� //�W����ܶR���V 
    tinyint DecInPrice;          //С���� //�p���I 
} SPApiPos;

typedef struct
{
    double Price;              //�۸� //���� ��
    double StopLevel;          //ֹ��۸� //��l���� ��
    double UpLevel;            //����ˮƽ //�W������ 
    double UpPrice;            //���޼۸� //�W������ ��
    double DownLevel;          //����ˮƽ //�U������ 
    double DownPrice;          //���޼۸� //�U������ ��
    bigint ExtOrderNo;         //�ⲿָʾ //�~������ 
    long IntOrderNo;           //�û�������� //�Τ�q��s�� 
    long Qty;                  //ʣ���� //�ѤU�ƶq
    long TradedQty;            //�ѳɽ����� //�w����ƶq 
    long TotalQty;             //����������//�q���`�ƶq 2012-12-20 xiaolin
    long ValidTime;            //��Чʱ�� //���Įɶ� 
    long SchedTime;            //Ԥ������ʱ�� //�w�q�o�e�ɶ� �ȤB
    long TimeStamp;            //���������ն���ʱ�� //�A�Ⱦ������q��ɶ� 
    u_long OrderOptions;       //����ú�Լ֧�����к��ڻ�����ʱ��(T+1),�ɽ���������Ϊ:1 //�p�G�ӦX�������������f����ɬq(T+1),�i�N���ݩʳ]��:1 
    STR16 AccNo;               //�û��ʺ� //�Τ�b�� 
    STR16 ProdCode;            //��Լ���� //�X���N�� 
    STR16 Initiator;           //�µ��û� //�U��Τ�  
    STR16 Ref;                 //�ο� //�Ѧ� 
    STR16 Ref2;                //�ο�2 //�Ѧ�2 
    STR16 GatewayCode;         //���� //���� 
    STR40 ClOrderId;           //�û��Զ������ο�//�Τ�۩w�q��Ѧ� 2012-12-20 xiaolin
    char BuySell;              //�������� //�R���V 
    char StopType;             //ֹ������ //��l����  
    char OpenClose;            //��ƽ�� //�}����  
    tinyint CondType;          //������������ //�q��������� 
    tinyint OrderType;         //�������� //�q������  
    tinyint ValidType;         //������Ч���� //�q�榳������ 
    tinyint Status;            //״̬ //���A 
    tinyint DecInPrice;        //��ԼС��λ //�X���p�Ʀ� 
} SPApiOrder;

typedef struct
{
	long RecNo;		   //�ɽ���¼
    double Price;              //�ɽ��۸� //�������
	double AvgPrice;           //�ɽ�����
    bigint TradeNo;            //�ɽ���� //����s��
    bigint ExtOrderNo;         //�ⲿָʾ //�~������
    long IntOrderNo;           //�û�������� //�Τ�q��s��
    long Qty;                  //�ɽ����� //����ƶq
    long TradeDate;            //�ɽ����� //������
    long TradeTime;            //�ɽ�ʱ�� //����ɶ�
    STR16 AccNo;               //�û� //�Τ�
    STR16 ProdCode;            //��Լ���� //�X���N�X
    STR16 Initiator;           //�µ��û� //�U��Τ�
    STR16 Ref;                 //�ο� //�Ѧ�
    STR16 Ref2;                //�ο�2 //�Ѧ�2
    STR16 GatewayCode;         //���� //����
    STR40 ClOrderId;           //�û��Զ������ο�//�Τ�۩w�q��Ѧ� 2012-12-20 xiaolin
    char BuySell;              //�������� //�R���V
    char OpenClose;            //��ƽ�� //�}����
    tinyint Status;            //״̬ //���A
    tinyint DecInPrice;        //С��λ //�p�Ʀ�
} SPApiTrade;

#define REQMODE_UNSUBSCRIBE     0
#define REQMODE_SUBSCRIBE       1
#define REQMODE_SNAPSHOT        2


typedef struct
{
    double Margin;			//��֤��//�O�Ҫ�
    long ContractSize;		//��Լ��ֵ//�X������
    STR16 MarketCode;		//���������� //�����N�X
    STR16 InstCode;			//��Ʒϵ�д��� //���~�t�C�N�X
    STR40 InstName;			//Ӣ������ //�^��W��
    STR40 InstName1;		//�������� //�c��W��
    STR40 InstName2;		//�������� //²��W��
    STR4 Ccy;				//��Ʒϵ�еĽ��ױ��� //���~�t�C���������
    char DecInPrice;		//��Ʒϵ�е�С��λ //���~�t�C���p�Ʀ�
    char InstType;			//��Ʒϵ�е����� //���~�t�C������
} SPApiInstrument;

typedef struct
{
   STR16 ProdCode;			//��Ʒ���� //���~�N�X
   char ProdType;			//��Ʒ���� //���~����
   STR40 ProdName;			//��ƷӢ������ //���~�^��W��
   STR16 Underlying;		//�������ڻ���Լ//���p�����f�X��
   STR16 InstCode;			//��Ʒϵ������ //���~�t�C�W��
   long ExpiryDate;			//��Ʒ����ʱ�� //���~����ɶ�
   char CallPut;			//��Ȩ�����Ϲ����Ϲ� //���v��V�{�ʻP�{�f
   long Strike;				//��Ȩ��ʹ��//���v��ϻ�
   long LotSize;			//����//���
   STR40 ProdName1;			//��Ʒ�������� //���~�c��W��
   STR40 ProdName2;			//��Ʒ�������� //���~²��W��
   char OptStyle;			//��Ȩ������//���v������
   long TickSize;			//��Ʒ�۸���С�仯λ��//���~����̤p�ܤƦ��
}SPApiProduct;

#define SP_MAX_DEPTH    20
#define SP_MAX_LAST     20
typedef struct
{
    double Bid[SP_MAX_DEPTH];     //����� //�R�J��
    long BidQty[SP_MAX_DEPTH];    //������ //�R�J�q
    long BidTicket[SP_MAX_DEPTH]; //��ָ������ //�R���O�ƶq
    double Ask[SP_MAX_DEPTH];     //������ //��X��
    long AskQty[SP_MAX_DEPTH];    //������ //��X�q
    long AskTicket[SP_MAX_DEPTH]; //��ָ������ //����O�ƶq
    double Last[SP_MAX_LAST];     //�ɽ��� //�����
    long LastQty[SP_MAX_LAST];    //�ɽ����� //����ƶq
    long LastTime[SP_MAX_LAST];   //�ɽ�ʱ�� //����ɶ�
    double Equil;                 //ƽ��� //���Ż�
    double Open;                  //���̼� //�}�L��
    double High;                  //��߼� //�̰���
    double Low;                   //��ͼ� //�̧C��
    double Close;                 //���̼� //���L��
    long CloseDate;               //�������� //�������
    double TurnoverVol;           //�ܳɽ��� //�`����q
    double TurnoverAmt;           //�ܳɽ��� //�`�����B
    long OpenInt;                 //δƽ�� //������
    STR16 ProdCode;               //��Լ���� //�X���N�X
    STR40 ProdName;               //��Լ���� //�X���W��
    char DecInPrice;              //��ԼС��λ //�X���p�Ʀ�
} SPApiPrice;

typedef struct
{
    double Price;              //�۸� //����
    long Qty;                  //�ɽ��� //����q
    long TickerTime;           //ʱ�� //�ɶ�
    long DealSrc;              //��Դ //�ӷ�
    STR16 ProdCode;            //��Լ���� //�X���N�X
    char DecInPrice;           //С��λ //�p�Ʀ�
} SPApiTicker;

typedef struct
{
	double NAV;               // �ʲ���ֵ				//add xiaolin 2013-03-19
    double BuyingPower;       // ������					//add xiaolin 2013-03-19
    double CashBal;           // �ֽ����				//add xiaolin 2013-03-19
	double MarginCall;        //׷�ս��
    double CommodityPL;       //��Ʒӯ��
    double LockupAmt;         //������
    double CreditLimit;       //�Ŵ��޶� // �H�U���B
    double MaxMargin;         //��߱�֤�� // �̰��O����//modif xiaolin 2012-12-20 TradeLimit
    double MaxLoanLimit;      //��߽������ // �̰��ɶU�W��
    double TradingLimit;      //���ý����~ // �H�Υ���B
    double RawMargin;         //ԭʼ���C�� // ��l�O�Ҫ�
    double IMargin;           //�������^�� //  �򥻫O����
    double MMargin;           //�S�ֱ��^�� // �����O����
    double TodayTrans;        //���׽��~ // ������B
    double LoanLimit;         //�Cȯ�ɰ���ֵ // �Ҩ�i���`��
    double TotalFee;          //�M�ÿ��~ //  �O���`�B
    double LoanToMR;	      //���/�ɰ�ֵ%
    double LoanToMV;	      //���/��ֵ%    
    STR16 AccName;            //�������Q //  ��f�W��
    STR4 BaseCcy;             //����؛�� // �򥻳f��
    STR16 MarginClass;        //���^��e // �O�������O
    STR16 TradeClass;         //����e // ������O
    STR16 ClientId;           //�͑� // �Ȥ�
    STR16 AEId;               //���o //  �g��
    char AccType;             //����e // ��f���O
    char CtrlLevel;           //���Ƽ��� //  ����ż�
    char Active;              //��Ч //  �ͮ�
    char MarginPeriod;        //�r�� // �ɬq
} SPApiAccInfo;

typedef struct
{
    double CashBf;          //���ս��� //�W�鵲�l
    double TodayCash;       //���մ�ȡ //����s��
    double NotYetValue;     //δ���� //���榬
    double Unpresented;     //δ���� //���I�{
    double TodayOut;        //��ȡҪ�� //�����n�D
    STR4 Ccy;               //���� //�f��
} SPApiAccBal;

typedef struct
{
    STR4 Ccy;
    double Rate;
} SPApiCcyRate;


#define SPDLLCALL __stdcall
/*�ص�����*/
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

/*���󷽷�*/
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

