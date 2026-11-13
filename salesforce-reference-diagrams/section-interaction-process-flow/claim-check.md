---
title: Claim Check | Interaction Process Flow | Reference Diagrams | Salesforce Architects
source: https://architect.salesforce.com/docs/architect/reference-diagrams/guide/claim-check.html
section: section-interaction-process-flow
---
  

# Claim Check

 

![claim check - shows an event being published when a record is modified. The message body of the event is stored in a separate data store while the header, which contains a claim check is passed onto a subscriber. The subscriber then uses the claim check to retrieve the message body when it's ready to process the information when necessary.](images/claim-check.webp)

  

This diagram shows the claim check pattern. This pattern publishes and event to an event bus when a record is modified. The message body of the event is stored in a separate data store while the header, which contains a claim check, is passed onto a subscriber. The subscriber then uses the claim check to retrieve the message body when it’s ready to process the information.

  
 
- [Lucid](https://lucid.app/lucidchart/editNewOrRegister/0699a470-11ca-4291-88d6-a6399142a1ca) 
- [Image](https://architect.salesforce.com/ns-assets/reference-architectures/claim-check.webp) 
   