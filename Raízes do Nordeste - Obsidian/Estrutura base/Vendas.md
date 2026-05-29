
* O sistema não processará pagamentos no app principal, e deverá apenas:
	* Solicitar pagamento
	* Receber confirmação ou negação
	* Registrar o resultado
	* Atualizar status do pedido
* O pagamento será feito com arquitetura de integração com sistema de pagamento
	* Reduz risco
	* Aumenta segurança
	* Melhora escalabilidade
	* Exige cuidado na modelagem e tratamento de falhas