/*
 * App.c
 *
 *  Created on: Jan 16, 2020
 *      Author: Ericson Joseph
 */

#include "App.h"
#include "FreeRTOSConfig.h"
#include "cmsis_os.h"
#include "ethernetif.h"
#include "lwip/netif.h"
#include "lwip/tcpip.h"
#include "httpserver_netconn.h"
#include "app_ethernet.h"

struct netif gnetif; /* network interface structure */

static void APP_Task(const void *arg);
static void Netif_Config(void);

void APP_Init() {

	BSP_LED_Init(LED1);
	BSP_LED_Init(LED2);
	BSP_LED_Init(LED3);
	BSP_LED_Init(LED4);

	osThreadDef(App_Thread, APP_Task, osPriorityNormal, 0, configMINIMAL_STACK_SIZE*5);
	osThreadCreate(osThread(App_Thread), NULL);

}

void APP_Task(const void *arg) {

	/* Create tcp_ip stack thread */
	tcpip_init(NULL, NULL);

	/* Initialize the LwIP stack */
	Netif_Config();

	/* Initialize webserver demo */
	http_server_netconn_init();

	for (;;) {
		/* Delete the Init Thread */
		osThreadTerminate(NULL);
	}
}

/**
 * @brief  Initializes the lwIP stack
 * @param  None
 * @retval None
 */
static void Netif_Config(void) {
	ip_addr_t ipaddr;
	ip_addr_t netmask;
	ip_addr_t gw;

#if LWIP_DHCP
	ip_addr_set_zero_ip4(&ipaddr);
	ip_addr_set_zero_ip4(&netmask);
	ip_addr_set_zero_ip4(&gw);
#else
  IP_ADDR4(&ipaddr,IP_ADDR0,IP_ADDR1,IP_ADDR2,IP_ADDR3);
  IP_ADDR4(&netmask,NETMASK_ADDR0,NETMASK_ADDR1,NETMASK_ADDR2,NETMASK_ADDR3);
  IP_ADDR4(&gw,GW_ADDR0,GW_ADDR1,GW_ADDR2,GW_ADDR3);
#endif /* LWIP_DHCP */

	/* add the network interface */
	netif_add(&gnetif, &ipaddr, &netmask, &gw, NULL, &ethernetif_init,
			&tcpip_input);

	/*  Registers the default network interface. */
	netif_set_default(&gnetif);

	ethernet_link_status_updated(&gnetif);

#if LWIP_NETIF_LINK_CALLBACK
  netif_set_link_callback(&gnetif, ethernet_link_status_updated);

  osThreadDef(EthLink, ethernet_link_thread, osPriorityNormal, 0, configMINIMAL_STACK_SIZE *2);
  osThreadCreate (osThread(EthLink), &gnetif);
#endif

#if LWIP_DHCP
	/* Start DHCPClient */
	osThreadDef(DHCP, DHCP_Thread, osPriorityBelowNormal, 0, configMINIMAL_STACK_SIZE * 2);
  osThreadCreate (osThread(DHCP), &gnetif);
#endif
}
