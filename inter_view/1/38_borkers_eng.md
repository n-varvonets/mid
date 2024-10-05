# Interview Preparation Summary - Concise Responses

### **1. Coding Standards**
- **SOLID Principles**:
  - **SRP**: One reason for change per class.
  - **OCP**: Code should be extendable without modification.
  - **LSP**: Derived classes must replace base classes without altering behavior.
  - **ISP**: Avoid forcing clients to use unneeded interfaces.
  - **DIP**: Depend on abstractions, not concrete implementations.

  **Detailed Explanation**: SOLID principles help maintain clean and scalable code:
  - SRP and ISP ensure minimal and specific class responsibilities.
  - OCP and DIP make code easily extendable and modular.
  - LSP ensures inheritance follows logical substitution, maintaining consistency.

- **YAGNI**: Avoid adding features until you actually need them to reduce unnecessary code complexity.


### **4. Best Practices**
- **Microservices**:
  - **Concepts**: Decompose monoliths into independently deployable services; ensure **service discovery**, use **API gateways**, implement **circuit breakers** for reliability, and handle **data consistency** challenges.
  - **Detailed Explanation**: Microservices provide scalability, fault isolation, and independent development. The main challenges involve managing distributed data and ensuring inter-service communication remains efficient and reliable.

- **OOP Design Patterns**:
  - **Common Patterns**: Singleton, Factory, Observer, Strategy.
  - **Usage**: To improve code modularity and reusability.

- **Queuing Systems**:
  - Familiarity with **Celery** for distributed tasks and improving response time by offloading asynchronous work.

### **7. Databases and Message Brokers**
# ACID in SQL Databases

### **ACID Properties**:
**ACID** stands for **Atomicity**, **Consistency**, **Isolation**, and **Durability**. These are key properties of relational database transactions to ensure reliable processing:

1. **Atomicity**: 
   - Example: If a transaction involves transferring money between two accounts, both the debit and credit must occur, or neither should.

2. **Consistency**:
   - Ensures that a transaction transforms the database from one valid state to another, **maintaining all predefined rules** (such as constraints and relationships).
   - Example: If a bank account balance cannot be negative, consistency ensures that no transaction violates this rule.

3. **Isolation**:
   - Ensures that **concurrent transactions** do not interfere with each other. The outcome should be as if the transactions were executed sequentially.
   - Isolation levels (e.g., **Read Uncommitted**, **Read Committed**, **Repeatable Read**, **Serializable**) define how changes made by one transaction become visible to others.

4. **Durability**:
   - Guarantees that once a transaction is **committed**, it will persist, even in the event of a system failure.
   - Example: After committing a bank transfer, the changes are saved to disk, ensuring data is not lost if the database crashes afterward.

### **Summary**:
- **ACID properties** ensure **data integrity** and **reliability** in SQL databases, especially for complex operations involving multiple transactions or system crashes.
- **NoSQL**: Familiarity with **MongoDB**, **Redis** for caching, and session management.
- **Message Brokers**: 
  - **RabbitMQ**: Handling message queues, routing.
  - **Kafka**: Building event-driven, real-time systems.

### **8. Cloud and Infrastructure**
- **AWS**: Experience with **EC2**, **S3**, **RDS**, and **Lambda** for serverless computing.
- **CloudFormation**: Use IaC for resource management with YAML/JSON templates.
- **Docker**: Containerize applications; use **Docker Compose** for local environments.
- **CI/CD**: Implement Jenkins or GitLab CI for automated testing and deployments.

