---
title: Asynchronous Processing Via Platform Events | Interaction Process Flow | Reference Diagrams | Salesforce Architects
source: https://architect.salesforce.com/docs/architect/reference-diagrams/guide/asynchronous-processing-via-platform-events.html
section: section-interaction-process-flow
---
  

# Asynchronous Processing Via Platform Events

 

![asynchronous processing via platform events - shows how asynchronous processing works with platform events. The events published into the bus are delivered in order via publish after commit and then processed in bulk by a flow in a separate synchronous context.](images/asynchronous-processing-via-platform-events.webp)

  

The diagram illustrates an interaction process flow for asynchronous processing using platform events, showing how events are published into the event bus as part of a broader architecture pattern. This pattern is designed for scenarios where a process needs to trigger downstream work without blocking the main transaction, letting Salesforce handle the heavy lifting asynchronously.

  
 
- [Lucid](https://lucid.app/lucidchart/editNew/73e12d46-2c45-4d7c-bcf4-a2ca7596ed4c) 
- [Image](https://architect.salesforce.com/ns-assets/reference-architectures/asynchronous-processing-via-platform-events.webp) 
   