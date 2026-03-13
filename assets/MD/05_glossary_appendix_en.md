# Glossary

**Digital Asset \| Digital Asset :**

Refers to an asset that exists only in the form of digital data. It is generally associated with a right of use that can be transferred between users. Cryptocurrencies (CMs) are digital assets.

**Shared Archiving \| Shared Archiving :**

Refers to the process by which a set of records is replicated and distributed across a multitude of nodes in a network. This ensures that each participant has a local copy of the ledger, which is continuously updated and synchronized with the others.

**Merkle Tree \| Merkle Tree :**

A data structure in which each leaf node is a hash of a block of data, and each non-leaf node is a hash of its child nodes. It allows for efficient and secure verification of the contents of large data structures. See Appendix V.2.

**Blockchain \| Blockchain :**

This term, which has become commonplace, refers to a type of distributed ledger technology (DLT) where records are organized into a chronological chain of blocks, linked and secured using cryptography. Each block typically contains a cryptographic hash of the previous block, a timestamp, and transaction data. This design makes the ledger resistant to modification of its data.

**Central Bank Digital Currency (CBDC) \| Central Bank Digital Currency (CBDC) :**

A digital form of a country's fiat currency that is a direct liability of the central bank. Unlike cryptocurrencies, a CBDC is centralized and issued by a monetary authority.

**Target Difficulty \| Target Difficulty :**

In Proof of Work (PoW) based protocols, this is a value that the hash of a block header must be less than or equal to for the block to be considered valid. The difficulty is adjusted periodically to maintain a stable block production time.

**Client \| Client :**

Refers to the software that implements the protocol rules and allows a node to connect to the network, validate transactions and blocks, and interact with the distributed ledger.

**Source Code \| Source Code :**

A set of instructions written in a human-readable programming language. It is the basis of any software and must be compiled or interpreted to be executed by a computer.

**Community \| Community :**

Refers to the group of individuals and organizations that participate in the development, maintenance, and use of a distributed ledger protocol. This includes developers, users, miners, companies, and researchers.

**Consensus \| Consensus :**

A collective agreement process within a distributed network to validate and add new records to the ledger. It ensures that all nodes have an identical and consistent version of the ledger.

**Consistency \| Consistency :**

A property of distributed systems ensuring that all nodes in the network see the same data at the same time. In the context of DLTs, it means that all valid transactions will eventually be recorded in the same order on all nodes.

**Cryptocurrency (CM) \| Cryptocurrency (CC) :**

A type of digital or virtual currency that uses cryptography for security. It is decentralized and based on distributed ledger technology, such as a blockchain.

**Endogenous Data \| Endogenous Data :**

Data that is generated and exists only within the boundaries of the distributed ledger protocol. This includes transactions, account balances, and smart contract states.

**Exogenous Data \| Exogenous Data :**

Data originating from outside the distributed ledger system that can be integrated into it, often via oracles. This can include financial data, real-world events, or identity information.

**Record (or Block) \| Record (or Block) :**

For Bitcoin and Ethereum, it is customary to call it a "Block" - it represents a containerized set of transaction data, recognized by all nodes as canonical after each has verified its validity. A record is composed of a *block header* and the list of transactions it contains, i.e., the transactions processed and validated since the previous block, to which is usually added a transaction awarding a reward to the creator of this record.

**Genesis Record (or Genesis Block) \| Genesis Record (or Genesis Block) :**

This is the first record issued and broadcast within a distributed ledger protocol. It has a special status as it cannot refer to a previous record, unlike other records, nor to any transaction that preceded it. The genesis block is hardcoded into the original software and launches the protocol.

**Record header (or block header) \| Record header (or block header) :**

A record header is unique and serves to identify a particular record on a *ledger*. It is this record header that is hashed during the *proof of work* process. Under the Bitcoin protocol, *records* or *[blocks](https://en.bitcoin.it/wiki/Block)* are composed of a fixed-size header containing only the information necessary for the assembly of the ledger (or *blockchain*). Although this very limited size does not allow for storing all transactions, the header nevertheless contains the root of a *Merkle Tree*, which allows for verifying the presence of a specific transaction in the *ledger* without having to download its entirety.

**Scalability \| Scalability :**

The ability of a distributed ledger protocol system to handle a growing number of interactions efficiently without compromising its performance.

**Ledger explorer \| Ledger explorer :**

Refers to a tool offering a user interface to view the real-time data of a distributed ledger protocol. Facilitating transparency and transaction verification, it is an essential *off-chain* tool for users and developers who wish to track the activity and health of the network.

**On-chain transaction fees \| On-chain transaction fees :**

These are fees expressed and paid in the *native unit of account*, which the user defines when creating a transaction to interact *on-chain*. Generally, and beyond the differences between CMs and their fee mechanisms, the amount of transaction fees paid relative to other users determines how quickly that transaction will be processed: *transaction operators* tend to choose to process transactions with the highest fees, as they are the most profitable, since these transaction fees are added to the *block reward* to constitute the operating income of *transaction processing operators*. The use of *gateways* (exchange platforms, etc.) can induce, in addition to on-chain transaction fees, off-chain transaction fees, defined by the gateway's terms and conditions.

**Transaction finality \| Transaction finality :**

Refers to the point at which a confirmed record can be considered final and irreversible. It can be probabilistic, as with Bitcoin's PoW, where reversibility becomes computationally impossible after a few blocks. It can also be explicit, with protocols integrating checkpoints. In general, it is the economic actors accepting native units of account (NUAs) who define the number of confirmations necessary to consider a transaction as settled on their end.

**Hash function \| Hash function :**

Refers to a cryptographic function that, when applied to incoming raw data, encrypts it into a unique and partial digital fingerprint (a **Hash**), of a defined size, which allows for easy identification of the initial data. See Appendix V.3.

**Software Forge (conventionally referred to as « code base repo » or « GitHub repo ») \| Software Forge :**

A forge is a hosting platform for software projects, corresponding to a web environment that brings together a set of tools enabling collaborative and distributed software development. It offers a community portal and access to a website, a set of project management tools, and a collaborative development environment. The available services range from providing a version control system to trackers for submitting feature requests, bug tracking, task management; delivery of packages and files; continuous integration; document management (wiki); and other services (forums, mailing lists, polls, etc.).

**Fork \| Fork :**

Following the situation, it can qualify an event (voluntary or not) that sees a network split into two or more networks (*Chain Fork*), with as many different transaction ledgers. It is also generally used to qualify protocol modifications considered important, to evolve them in a desired direction (adding/removing features, changing architecture, etc.). A distinction is then made between *Soft Forks* and *Hard Forks*, as well as their more or less contentious nature. A chain fork can occur following a software bug, which then induces a loss of *consistency* of *endogenous data* since different software clients no longer follow the same protocol rules; (ii) or when a modification of the distributed ledger protocol is undertaken and not followed by all actors, giving rise to a contentious *Hard Fork*. These two branches of programs that have become incompatible give birth to two different distributed ledger protocols that exist autonomously, the Fork becoming a political means of emancipation and recomposition of actors around differentiated values and interests.

**Timestamp \| Timestamp :**

The process of recording the exact date and time at which an event occurs. It is commonly used in log files, databases, digital documents, and tracking systems to ensure data traceability and integrity.

**Off-chain \| Off-chain :**

Interactions, transactions, processes that occur outside the formal boundaries of the distributed ledger protocol.

**Local Journal \| Journal :**

Refers to a set of records logged locally in a node, which is not necessarily consistent with the consensus of other nodes. Local Journals are partial, provisional, and heterogeneous.

**Native Unit(s) of Account (NUA) \| Native currency(ies) :**

The unit(s) of account issued and administered within the protocol and typically used to regulate record production, pay network usage transaction fees, and conduct monetary policy to align the interests of stakeholders. Their scriptural forms follow the logic and format(s) of the considered protocol.

**Programming language \| Programming language :**

A formal notation used to define computer codes and have them executed by a program. It includes a set of instructions producing various types of results. The description of a programming language is generally divided into two parts: syntax (form) and semantics (meaning). They can be defined by a specification document or may only relate to a dominant implementation treated as a reference. Developers can use many programming languages with different characteristics to create source codes that still need to be compiled to be translated into low-level machine language. This machine language, the native language of a processor, corresponds only to instructions coded in binary. E.g.: C++, Python, JavaScript, Solidity, Bytecode, etc.

**White Paper (WP) \| White Paper (WP) :**

A name originating from English political life, where documents printed on white paper were used to present government policies and submit them for public opinion. This term has been used by companies to describe certain projects or commercial policies. In our field, it refers to a publication of varying length, which aims to provide a sum of information on a given project. The White Paper serves to expose an objective as well as the proposed means to solve it. Published by the project's instigator(s), it may also contain information on the project's financing, a roadmap, an indicative budget, and a description of the team working on the development. A WP does not necessarily go into deep technical details; thus, Yellow Papers may be published. The latter correspond to a more technical version of the WP, where the technological, and even scientific, details of the project are presented.

**Maximalist (Bitcoiner) \| Maximalist (Bitcoiner) :**

A term that appeared in 2014, often attributed to Vitalik Buterin (2014). It refers to Bitcoiners for whom Bitcoin should dominate all other CMs (qualified as "altcoins" or "shitcoins"), considered inferior or useless. They believe that an environment of multiple competing CMs is not desirable and that all innovations and development in the crypto field should be done exclusively on Bitcoin. By extension, the term *maximalist* can also refer to fervent supporters of a specific cryptocurrency who reject all others.

**Digital Money \| Digital Money :**

A generic category covering currencies based on distributed ledger technology, but not limited to cryptocurrencies (CMs). It encompasses many objects falling under the logic of signature or seal, depending on the existence of central actors with exorbitant rights over the protocol, data, and network. Within it, one can distinguish, in addition to CMs, units of account issued by private entities, such as Tether, which are private digital currencies, and public currencies, with the advent of central bank digital currencies (CBDCs), whose trust is based on a public issuing authority. See box in Chap.II.3.

**Node \| Node :**

In general, this term covers non-human actors and their human operators participating in the network, communicating with their peers according to the canonical rules of the considered distributed ledger protocol. They can take different forms and, depending on these, take part in all or part of the processes related to transaction processing and record production or their verification: mining nodes, full nodes, etc.

**Nonce \| Nonce :**

In cryptography, this corresponds to an arbitrary number (random or pseudo-random) intended to be used only once. Regarding *proof of work* functions, some processes require providing a nonce which, combined with the data block input into a hash function, provides a result with certain desired characteristics, making it much more difficult to create a target result than to verify it. For Bitcoin, it is this nonce that is modified by transaction operators with each *proof of work* attempt, until a *digital fingerprint* of the record is obtained that is less than or equal to the *target difficulty*. Thus, the activity of transaction operators is to be the first to find the *nonce* that, combined with the initial data of the *candidate record*, allows for obtaining a valid digital fingerprint. The *nonce* can have a different meaning for Ethereum because, in addition to the previous sense, it also corresponds to the numbering of transactions performed and processed by an account.

**Gateway \| Gateway :**

Contains all the actors that provide an interface between the distributed ledger protocol system and the outside world. This includes crypto-fiat exchange platforms that offer a monetary gateway, but also many other services such as *ledger explorers*, for example.

**Proof of Work (PoW) \| Proof of Work (PoW) :**

Corresponds to a process requiring the resolution of a cryptographic challenge: obtaining a cryptographic fingerprint of a given difficulty level. For ledger protocols whose consensus is based on Proof of Work, this process is called "mining," and the operators who carry it out are the "miners."

**Wallet \| Wallet :**

Corresponds to a client software capable of generating, storing, and managing pairs of cryptographic keys in order to store and transfer its CMs and digital assets.

**Protocol \| Protocol :**

A set of standardized rules and procedures allowing networked machines to communicate with each other. It determines, for a given system, the modalities of its operation.

**Double-spending problem \| Double-spending problem :**

A problem faced by any digital currency. It corresponds to a fraudulent act whereby a unit of account, due to its digital nature, is falsifiable and duplicable, and can be spent more than once. As with counterfeit money, such a practice can increase the money supply and erode user trust in the payment system.

**Block reward \| Block reward :**

Corresponds to a reward in *native unit of account* received by a transaction operator whose *candidate record* becomes canonical by being integrated into the *ledger*. It plays the role of monetary creation, remunerating actors in return for the work of processing and securing transactions and the *ledger*.

**Ledger \| Ledger :**

Corresponds, at any given time, to the set of authoritative records, logged in a substantial portion of the nodes participating in the network. A *ledger* consists of a series of different records storing information related to the transactions that take place on the network. The records integrated into such a ledger are unlikely to be erased or modified, and are considered final. See *transaction finality*.

**Record reorganization \| Record reorganization :**

This is a normal event in any distributed ledger protocol where a network node discovers that another valid record exists in parallel to the one it is following. Through the consensus algorithm and following a new record production cycle, this alternative version of the ledger has become canonical for everyone, excluding one or more previously included record(s), said to be "orphan(s)". The 51% attack extensively discussed by Nakamoto refers to a critical case of this phenomenon where an entity with more than 51% of the computing power can secretly prepare a competing valid and heavier history than the one currently considered canonical, in order to profit from the cancellation of transactions made within the orphaned history. See Appendix V.5.

**Network \| Network :**

Corresponds to the set of actors - human or not - and interconnected processes that implement a communication protocol between different machines or *nodes* allowing them to exchange information. The most widespread networks operate on the "client/server" communication mode, where a computer and its user - the client - request information by issuing a query to a central server that has it and transmits it back. This is the case for browsers and a large majority of websites, for example. Other forms exist such as *peer-to-peer networks*.

**Peer-to-peer Network \| Peer-to-peer Network :**

Corresponds to a *network* where the *nodes* participating in the information exchange are, unlike the "client/server" mode, alternately client and server, requester and provider. Each *node* is on an equal footing with the other *nodes* constituting the *network*, and they are therefore peers. There is no longer one actor who has the information that a multitude of users wish to access, because the information is replicated on a multitude of *nodes*.

**Censorship Resistance \| Censorship Resistance :**

Corresponds to the impossibility for an actor or a cartel to unilaterally and arbitrarily: (i) modify the protocol rules; (ii) block or censor transactions; and (iii) seize an account or freeze assets.

**Programmatically-executed script \| Programmatically-executed script :**

A computer script that, when triggered by a particular message, is executed by the distributed ledger protocol. When the code is able to operate according to the expectations of the engaged parties, the deterministic nature of the execution reduces the level of trust required by individual participants in their reciprocal interactions. They are commonly called "Smart Contracts" because of the ability of scripts to replace certain contractual or fiduciary relationships, such as custody or escrow, with code. However, they are neither autonomous, nor adaptive ("intelligent"), and even less a contract in the legal sense of the term.

**Cryptographic signature \| Cryptographic signature :**

Based on asymmetric cryptography, this type of signature allows for the mathematical verification of the possession of a set of data, provided that the user keeps their private key secret to sign their transactions. See Appendix V.1.

**Unspent Transaction Output (UTXO) \| UTXO :**

The form taken by received but not yet spent units of account for distributed ledger protocol systems that, like Bitcoin, operate on this type of architecture: here, the state of the *endogenous data* structure, contained in the *ledger* at a given time T, represents the collection of all existing UTXOs. Thus, a transaction corresponds to an authenticated transfer of one or more UTXOs (which are at the *output* of the transaction) and which will result, in output, in a UTXO received by the receiver (for them, in *input*). Other architectures can be chosen for tracking the state of the data structure, as with Ethereum and its *account-based model*.

**Account-based Model \| Account-based Model :**

The account-based model, like the UTXO-based model, is primarily used for tracking the state of the data structure. But here, as with a traditional bank account, at a given time T, the distributed ledger protocol system reports balances for each account. An authenticated transaction then corresponds to a transfer that reduces the sender's balance by the amount the receiver receives in their account. This choice by Ethereum is explained by the fact that, in addition to personal accounts - or externally owned accounts (EOAs) - controlled by a private key, there are accounts controlled by a contract command/code (the *smart contracts*, SCs). The account-based model then meets specific needs and allows for increasing the execution capacity of the *smart contracts* of the distributed ledger protocol that makes this choice (greater simplicity, space saving, increased fungibility).

**Distributed Ledger Technology (DLT) system \| DLT system :**

An electronic recording system that allows a network of independent participants to establish a consensus around an authoritative ordering of cryptographically validated transactions. The records are made persistent by replicating the data across a multitude of nodes, and are tamper-evident through the cryptographic links that connect them (hashes). The shared result of the reconciliation/consensus process constitutes a canonical transactional ledger that is authoritative.

**Permissioned System \| Permissioned System :**

A "Classic" type of distributed ledger protocol, as it was the first to be developed. This system corresponds to the general definition of DLTs; *shared archiving* is not open to everyone and only formally recognized and authorized participants can participate. This selection is made by the competent authority(ies) -- the entity(ies) that design and deploy the system -- and written into the software code provided by the administrators.

**Permissionless System \| Permissionless System :**

A distributed ledger protocol that underlies what we consider and qualify as CMs. In this type of system, *shared archiving* is open to all without any entity or group being granted any protocol-level privilege.

**Block time \| Block time :**

Block time refers to the average time required to create (or mine) a new block on the blockchain and complete a transaction processing cycle. For Bitcoin, the average block time is about 10 minutes.

**Partitioning Tolerance \| Partitioning Tolerance :**

Corresponds to a property sought by any distributed computing system allowing that no failure - with the exception of a total network outage - of one or more node(s) prevents the system from responding correctly.

**Transaction processing \| Transaction processing :**

Corresponds to the set of processes that specify the mechanisms for updating the ledger. It defines: (i) which participants have the right to update the set of shared authoritative records (without permission for open systems and with formal permission for private or consortium systems), and (ii) how participants reach a consensual agreement on the implementation of this update. Also called "mining."

**Transaction \| Transaction :**

Refers to any proposed change to the ledger; it is not necessarily of an economic nature (transfer of value). A transaction can be either unconfirmed (not included in the ledger, it is still only in the mempool), or confirmed (included in the ledger). A single transaction can contain a multitude of different transactions: different receivers; different ledger modifications, etc.

**Validation \| Validation :**

Corresponds to the set of processes required to ensure that actors independently reach the same conclusion regarding the state of the ledger. This includes verifying the validity of unconfirmed transactions, verifying records, whether confirmed or not, and auditing the state of the system.

**Independent Validation \| Independent Validation :**

Refers to the ability of the distributed ledger protocol system to allow each participant to independently verify the state of transactions and the integrity of the system.

# Appendices

# Table of Contents

[Appendix I: Synthetic data on the CM ecosystem as a whole](#appendix-i-synthetic-data-on-the-cm-ecosystem-as-a-whole)

[Appendix I.1: Total capitalization and dominance rate in the crypto-asset market (~5868 assets listed on Coingecko), as of 09/01/2020](#appendix-i.1-total-capitalization-and-dominance-rate-in-the-crypto-asset-market-~5868-assets-listed-on-coingecko-as-of-09/01/2020)

[Appendix I.2: Total capitalization and market dominance rate of crypto-assets (~5868 assets listed), as of 09/01/2020](#appendix-i.2-total-capitalization-and-market-dominance-rate-of-crypto-assets-~5868-assets-listed-as-of-09/01/2020)

[Appendix I.3: Evolution of the number of users on the Coinbase platform](#appendix-i.3-evolution-of-the-number-of-users-on-the-coinbase-platform)

[Appendix I.4: Detailed chronologies of the Initial Coin Offering (ICO) phenomenon, from July 2013 to June 2017](#appendix-i.4-detailed-chronologies-of-the-initial-coin-offering-ico-phenomenon-from-july-2013-to-june-2017)

[Appendix II: Synthetic data on the Bitcoin ecosystem](#appendix-ii-synthetic-data-on-the-bitcoin-ecosystem)

[Appendix II.1: The BTC NUA and its decimalization (material and symbolic)](#appendix-ii.1-the-btc-nua-and-its-decimalization-material-and-symbolic)

[Appendix II.2: Total number of transactions per day](#appendix-ii.2-total-number-of-transactions-per-day)

[Appendix II.3: Number of active addresses per day](#appendix-ii.3-number-of-active-addresses-per-day)

[Appendix II.4: Number of new addresses per day](#appendix-ii.4-number-of-new-addresses-per-day)

[Appendix II.5: Total number of addresses with a non-zero balance](#appendix-ii.5-total-number-of-addresses-with-a-non-zero-balance)

[Appendix II.6: Total value of transactions in BTC and USD, daily](#appendix-ii.6-total-value-of-transactions-in-btc-and-usd-daily)

[Appendix II.7: Average and median value of transactions in BTC and USD, daily](#appendix-ii.7-average-and-median-value-of-transactions-in-btc-and-usd-daily)

[Appendix II.8: Total value of the money supply in BTC and USD, daily](#appendix-ii.8-total-value-of-the-money-supply-in-btc-and-usd-daily)

[Appendix II.9: Daily issuance rate of the money supply and its inflation rate](#appendix-ii.9-daily-issuance-rate-of-the-money-supply-and-its-inflation-rate)

[Appendix II.10: Average and median transaction fees, in BTC and USD, daily](#appendix-ii.10-average-and-median-transaction-fees-in-btc-and-usd-daily)

[Appendix II.11: Cumulative income of "miners" in USD](#appendix-ii.11-cumulative-income-of-miners-in-usd)

[Appendix II.12: Cumulative Hash/s quantity and BTC price, in USD, daily](#appendix-ii.12-cumulative-hash/s-quantity-and-btc-price-in-usd-daily)

[Appendix II.13: Evolution of the Bitcoin electricity consumption index, in annualized TWH](#appendix-ii.13-evolution-of-the-bitcoin-electricity-consumption-index-in-annualized-twh)

[Appendix II.14: Volatility of the BTC NUA, in USD over 30, 60, and 180 days](#appendix-ii.14-volatility-of-the-btc-nua-in-usd-over-30-60-and-180-days)

[Appendix III: Synthetic data on the Ethereum ecosystem](#appendix-iii-synthetic-data-on-the-ethereum-ecosystem)

[Table III.1: The Ether NUA and its decimalization (material and symbolic)](#table-iii.1-the-ether-nua-and-its-decimalization-material-and-symbolic)

[Appendix IV: Data on our fieldwork](#appendix-iv-data-on-our-fieldwork)

[Appendix IV.1: List of our 27 ethnographic participations](#appendix-iv.1-list-of-our-27-ethnographic-participations)

[Appendix IV.2: List of our 20 semi-structured interviews](#appendix-iv.2-list-of-our-20-semi-structured-interviews)

[Appendix IV.3: Status(es) and Role(s) covered by the actors in our interviews](#appendix-iv.3-status(es)-and-role(s)-covered-by-the-actors-in-our-interviews)

[Appendix V: Technical and computer-related annexes](#appendix-v-technical-and-computer-related-annexes)

[Appendix V.1: Asymmetric cryptography](#appendix-v.1-asymmetric-cryptography)

[Appendix V.2: Merkle Tree](#appendix-v.2-merkle-tree)

[Appendix V.3: Hash function](#appendix-v.3-hash-function)

[Appendix V.4: Simplified Payment Verification (SPV)](#appendix-v.4-simplified-payment-verification-spv)

[Appendix V.5: The 51% attack](#appendix-v.5-the-51%-attack)

# Appendix I: Synthetic data on the CM ecosystem as a whole

## Appendix I.1: Total capitalization and dominance rate in the crypto-asset market (~5868 assets listed on Coingecko), as of 09/01/2020

| ![](media/image1.png) | ![](media/image2.png) |
|---|---|

## Appendix I.2: Total capitalization and market dominance rate of crypto-assets (~5868 assets listed), as of 09/01/2020

| ![](media/image3.png) | ![](media/image4.png) |
|---|---|

## Appendix I.3: Evolution of the number of users on the Coinbase platform

| ![](media/image5.png) |
|---|

## Appendix I.4: Detailed chronologies of the Initial Coin Offering (ICO) phenomenon, from July 2013 to June 2017

| ![](media/image6.png) | ![](media/image7.png) |
|---|---|

# Appendix II: Synthetic data on the Bitcoin ecosystem

## Table II.1: The BTC NUA and its decimalization (material and symbolic)

| **Bitcoin and its NUA Bitcoin** | |
|---|---|
| ![A picture containing text Description automatically generated](media/image8.png) ![A picture containing text, font, screenshot, line Description automatically generated](media/image9.png) | |
| **BTC** | |
| **₿** | |
| **Conventional fractional unit(s)** | **Value in NUA (BTC)** |
| The "***bitcoin***" | 1 (or 10^8^ satoshis) |
| The "***millibitcoin***" | 0.001 |
| The "***microbitcoin***" | 0.000001 |
| The "***satoshi***" | 0.00000001 |

## Appendix II.2: Total number of transactions per day ^(1)^ | ## Appendix II.3: Number of active addresses per day ^(2)^
|---|---|
| ![](media/image11.png) (from January 2009 to December 2019, logarithmic scale) | ![](media/image13.png) (from January 2009 to December 2019, logarithmic scale) |

## Appendix II.4: Number of new addresses per day ^(3)^ | ## Appendix II.5: Total number of addresses with a non-zero balance ^(4)^
|---|---|
| ![](media/image15.png) (from January 2009 to December 2019, logarithmic scale) | ![](media/image17.png) (from January 2009 to December 2019, logarithmic scale) |

## Appendix II.6: Total value of transactions in BTC and USD, daily ^(1)^ | ## Appendix II.7: Average and median value of transactions in BTC and USD, daily ^(2)^
|---|---|
| ![](media/image19.png) (from January 2009 to December 2019, logarithmic scale) | ![](media/image21.png) (from January 2009 to December 2019, logarithmic scale) |

## Appendix II.8: Total value of the money supply in BTC and USD, daily ^(3)^ | ## Appendix II.9: Daily issuance rate of the money supply and its inflation rate ^(4)^
|---|---|
| ![](media/image23.png) ![](media/image25.png) (from January 2009 to March 2019, logarithmic scale) | ![](media/image27.png) ![](media/image29.png) (from January 2009 to December 2019, logarithmic scale) |

## Appendix II.10: Average and median transaction fees, in BTC and USD, daily ^(3)^ | ## Appendix II.11: Cumulative income of "miners" in USD ^(4)^
|---|---|
| ![](media/image31.png) (from January 2009 to December 2019, logarithmic scale) | ![](media/image33.png) (from January 2009 to December 2019) |

## Appendix II.12: Cumulative Hash/s quantity ^(1)^ and BTC price, in USD, daily | ## Appendix II.13: Evolution of the Bitcoin electricity consumption index, in annualized TWH ^(2)^
|---|---|
| ![](media/image35.png) (from January 2009 to December 2019, logarithmic scale) | ![](media/image37.png) (from January 2009 to December 2019, logarithmic scale) |

## Appendix II.14: Volatility of the BTC NUA, in USD over 30, 60, and 180 days ^(3)^ | |
|---|---|
| ![](media/image39.png) (from January 2009 to March 2021) | |

# Appendix III: Synthetic data on the Ethereum ecosystem

## Table III.1: The Ether NUA and its decimalization (material and symbolic)

| **Ethereum and its NUA Ether** | |
|---|---|
| ![A picture containing triangle Description automatically generated](media/image41.png) ![A picture containing black, darkness Description automatically generated](media/image42.png) ![A picture containing triangle, Chart, Colorful character, line Description automatically generated](media/image43.png) | |
| **ETH** | |
| **Ξ** | |
| **Conventional fractional unit(s)** | **Value in NUA (ETH)** |
| The "***ether***" \| the "*ETH*" \| or the "*Buterin*" | 1 (or 10^18^ Wei) |
| The "***Milliether***" \| or the "*Finney*" | 0.001 |
| The "***Microether***" \| or the "*Szabo*" | 0.000001 |
| The "***Gwei***" \| or the "*Shannon*" | 0.000000001 |
| The "***Mwei***" \| or the "*Lovelace*" | 0.000000000001 |
| The "***Kwei***" \| or the "*Babbage*" | 0.000000000000001 |
| The "***Wei***" | 0.000000000000000001 |

# Appendix IV: Data on our fieldwork

## Appendix IV.1: List of our 27 ethnographic participations

| **#** | **Date** | **Event Type** | **Event Name** | **Duration (hours)** |
|---|---|---|---|---|
| **1** | 10-17-2017 | Bitcoin-Paris *Meet Up* | Social Meetup of Sofbar | 2 |
| **2** | 11-07-2017 | Bitcoin-Paris *Meet Up* | Social Meetup of Sofbar | 2 |
| **3** | 11-21-2017 | Bitcoin-Paris *Meet Up* | Presentation of the Tezos project | 2 |
| **4** | 12-05-2017 | Bitcoin-Paris *Meet Up* | Social Meetup of Sofbar | 2 |
| **5** | 12-12-2017 | Asseth *Meet Up* | Presentation of the Ethereum project | 2 |
| **6** | 01-09-2018 | Bitcoin-Paris *Meet Up* | Social Meetup of Sofbar | 2 |
| **7** | 01-16-2018 | Asseth *Meet Up* | Presentation of the Raiden project | 2 |
| **8** | 01-23-2018 | Bitcoin-Paris *Meet Up* | Presentation of the Lightning Network | 2 |
| **9** | 02-06-2018 | Bitcoin-Paris *Meet Up* | Social Meetup of Sofbar | 2 |
| **10** | 02-13-2018 | Asseth *Meet Up* | Presentation of the Gnosis project | 2 |
| **11** | 02-20-2018 | Bitcoin-Paris *Meet Up* | Presentation of the Woleet project | 2 |
| **12** | 03-06-2018 | Bitcoin-Paris *Meet Up* | Social Meetup of Sofbar | 2 |
| **13** | 03-13-2018 | Asseth *Meet Up* | Presentation of the MakerDAO project | 2 |
| **14** | 03-20-2018 | Bitcoin-Paris *Meet Up* | Presentation of the Samourai Wallet | 2 |
| **15** | 04-03-2018 | Bitcoin-Paris *Meet Up* | Social Meetup of Sofbar | 2 |
| **16** | 04-10-2018 | Asseth *Meet Up* | Presentation of the Kleros project | 2 |
| **17** | 04-17-2018 | Bitcoin-Paris *Meet Up* | Presentation of the Bisq project | 2 |
| **18** | 03-10-2018 | Ethereum Conference | EthCC 2018 | 12 |
| **19** | 05-25-2018 | Asseth *Meet Up* | Asseth hosts Parity + Snips at Talan Labs | 2 |
| **20** | 06-06-2018 | Bitcoin-Paris *Meet Up* | Social Meetup of Sofbar | 2 |
| **21** | 10-23-2018 | Book presentation and discussion | Presentation and signing of the book *Bitcoin Metamorphose* + discussion | 2 |
| **22** | 02-21-2019 | Dinner of the Cercle du Coin association | 42nd Coin Dinner | 3 |
| **23** | 03-05 to 03-07-2019 | Ethereum Conference | EthCC 2019 | 24 |
| **24** | 04-03-2019 | Bitcoin-Paris *Meet Up* | Social Meetup of Sofbar | 2 |
| **25** | 06-08 and 06-09-2019 | Bitcoin Conference | Breaking Bitcoin 2019 | 16 |
| **26** | 03-04-2020 | Bitcoin-Paris *Meet Up* | Social Meetup of Sofbar | 3 |
| **27** | 03-03 to 03-05-2020 | Ethereum Conference | EthCC 3 2020 | 24 |
| | | (average of about two each = ) | total | 124 |

## Appendix IV.2: List of our 20 semi-structured interviews

| **#** | **Name** | **Biography** | **Main Protocol** | **Modality** | **Date** |
|---|---|---|---|---|---|
| #1 | Adli Takkal Bataille | 34 years old; Self-taught, he has been passionate about computer science since a young age. He discovered Bitcoin in 2011 and became interested in it out of political conviction. He defines himself as a "cypherpunk" and a "Bitcoiner" who is very attached to the original vision of the protocol. In 2016, he co-founded the "Cercle du Coin," the first French-speaking association dedicated to Bitcoin and blockchains, of which he is the president. He is also the co-founder of the startup "Woleet," which offers data anchoring services on the Bitcoin blockchain. | Bitcoin | Videoconference | 01-15-2020 |
| | | | | Audio Recording | (65 min) |
| #2 | Antoine "Heilmo" F. | 28 years old; After studying computer science, he worked for several years as a developer in various companies. He discovered Bitcoin in 2013 and became interested in it for its technical and economic aspects. He is a developer and co-founder of the startup "Woleet." | Bitcoin | Videoconference | 01-16-2020 |
| | | | | Audio Recording | (55 min) |
| #3 | Pierre Noizat | 60 years old; A graduate of the École Polytechnique, he has had a long career in the telecommunications and internet sectors. He discovered Bitcoin in 2011 and founded the first French Bitcoin exchange, "Paymium," in 2011. He is also the author of several books on Bitcoin and cryptocurrencies. | Bitcoin | Face-to-face | 01-20-2020 |
| | | | | Audio Recording | (75 min) |
| #4 | Nicolas Cantu | 45 years old; A graduate of a business school, he worked for several years in the banking and financial sector. He discovered Bitcoin in 2013 and founded the "Chaintech" startup in 2016, which offers consulting and training services on blockchain technologies. | Bitcoin & Ethereum | Face-to-face | 01-21-2020 |
| | | | | Audio Recording | (90 min) |
| #5 | Gonzague Grandval | 30 years old; A graduate of a business school, he discovered Bitcoin in 2013. He is the co-founder of the "Paymium" exchange and the "Ledger" startup, which designs and markets physical cryptocurrency wallets. | Bitcoin | Face-to-face | 01-22-2020 |
| | | | | Audio Recording | (60 min) |
| #6 | Philippe Rodriguez | 52 years old; A serial entrepreneur, he has founded several companies in the internet and new technologies sectors. He discovered Bitcoin in 2013 and is the co-founder of the "Avolta Partners" consulting firm, which advises startups in their fundraising. | Bitcoin & Ethereum | Face-to-face | 01-23-2020 |
| | | | | Audio Recording | (70 min) |
| #7 | Hugo Renaudin | 26 years old; A graduate of a business school, he discovered Bitcoin in 2014. He is the co-founder of the "LGO" cryptocurrency exchange. | Bitcoin & Ethereum | Face-to-face | 01-24-2020 |
| | | | | Audio Recording | (45 min) |
| #8 | Jacques Favier | 65 years old; A graduate of HEC, he has had a long career in the banking and financial sector. He discovered Bitcoin in 2011 and is a very active member of the French-speaking community. He is the author of several books and articles on Bitcoin. | Bitcoin | Face-to-face | 01-27-2020 |
| | | | | Audio Recording | (120 min) |
| #9 | Manuel Valente | 40 years old; A computer engineer, he discovered Bitcoin in 2011. He is the co-founder of the "Maison du Bitcoin" (now "Coinhouse"), a physical space dedicated to cryptocurrencies in Paris. | Bitcoin | Face-to-face | 01-28-2020 |
| | | | | Audio Recording | (80 min) |
| #10 | Brian O'Hagan | 28 years old; A graduate of a business school, he discovered Bitcoin in 2013. He is the marketing director of the "Ledger" startup. | Bitcoin | Face-to-face | 01-29-2020 |
| | | | | Audio Recording | (50 min) |
| #11 | Grégory Guittard | 42 years old; A computer engineer, he discovered Bitcoin in 2011. He is the founder of the "Ark" blockchain project. | Ark | Videoconference | 01-30-2020 |
| | | | | Audio Recording | (60 min) |
| #12 | François-Xavier Thoorens | 40 years old; A computer engineer, he discovered Bitcoin in 2011. He is the co-founder of the "Ark" blockchain project. | Ark | Videoconference | 01-31-2020 |
| | | | | Audio Recording | (60 min) |
| #13 | Alexandre Stachtchenko | 28 years old; A graduate of a business school, he discovered Bitcoin in 2014. He is the co-founder of the "Chaintech" consulting and training firm. | Bitcoin & Ethereum | Face-to-face | 02-03-2020 |
| | | | | Audio Recording | (90 min) |
| #14 | Claire Balva | 28 years old; A graduate of a business school, she discovered Bitcoin in 2014. She is the co-founder of the "Chaintech" consulting and training firm. | Bitcoin & Ethereum | Face-to-face | 02-04-2020 |
| | | | | Audio Recording | (90 min) |
| #15 | Owen Simonin | 23 years old; Known as "Hasheur," he is a very popular French-speaking YouTuber specializing in cryptocurrencies. He discovered Bitcoin in 2016 and has since produced hundreds of videos on the subject. | Bitcoin & Ethereum | Videoconference | 02-05-2020 |
| | | | | Video Recording | (75 min) |
| #16 | William O'Rorke | 35 years old; A lawyer specializing in new technologies, he advises many companies in the blockchain sector. | Bitcoin & Ethereum | Face-to-face | 02-06-2020 |
| | | | | Audio Recording | (60 min) |
| #17 | Côme Prost-Boucle | 28 years old; A graduate of a business school, he discovered Bitcoin in 2017. He is the co-founder of the "LGO" cryptocurrency exchange. | Bitcoin & Ethereum | Face-to-face | 02-07-2020 |
| | | | | Audio Recording | (40 min) |
| #18 | David Prinçay | 38 years old; After a career in finance, he discovered Bitcoin in 2017. He is the director of the French branch of the "Binance" exchange. | Bitcoin & Ethereum | Videoconference | 02-10-2020 |
| | | | | Video Recording | (60 min) |
| #19 | Morgan Phuc | 35 years old; Studied mathematics and fluid mechanics. Destined to be an engineer, he started playing poker to finance his studies and became a professional player for nearly 11 years. He discovered Bitcoin and "cryptos" in late 2011 through a classmate, Benoist Huget. In late 2014, with B. Huget and his brother, he co-founded the startup and media "Bitconseil," which produces articles and practical resources related to the crypto ecosystem for French-speaking readers. He admits to having also been interested in Bitcoin due to its militant side, and declares himself close to "libertarian" thoughts. In 2017, M. Phuc and B. Huget developed a training activity, which they are in charge of. In 2018, they met and associated with "Bitconseil" the two co-founders of the *Journal Du Coin*, a media with a similar positioning that they subsequently decided to develop more strongly. The startup "BitConseil/Journal du Coin," which operates in the media, consulting, training, and events sector, now has a team of about fifteen people and M. Phuc is the content director and editor-in-chief, trainer, and, more sporadically than before, writer of articles on CMs and crypto-assets. | Bitcoin & Ethereum | Videoconference | 01-30-2020 |
| | | | | Video Recording | (127 min) |
| #20 | Antoine Le Calvez | 26 years old; Studied computer engineering, specializing in data analysis, at the University of Technology of Compiègne (Master's degree). He discovered Bitcoin and "cryptos" in early 2013, during his studies. His interest was directly guided by his interest and skills in data analysis, which were directly accessible to him, since these financial systems are "open" and "freely accessible." He began his *on-chain* data analysis activity on Bitcoin, with the publication of an information site titled "P2SH.info" (now txstats.com in collaboration with "Bitmex Research" and "Coinmetrics," where Mr. Le Calvez is an employee), which counted Bitcoin transactions using the "Pay to Script Hash" transaction format. It was this achievement that made him known, which allowed him to get in touch with companies in the sector interested in his skills. Thus, in 2016, he did his final year internship in London, at "Blockchain.info" -- one of the largest providers of online wallet services -- a company he left in 2018 to join the "Coinmetrics" team. He still works for this company today as a data scientist. | Bitcoin | Videoconference | 02-11-2020 |
| | | | | Video Recording | (85 min) |

## Appendix IV.3: Status(es) and Role(s) covered by the actors in our interviews

| **Interview #** | **"Developers"** | **"Transaction processing and verification operators"** | **Other Services (commercial or not)** | **End users** |
|---|---|---|---|---|
| | **Protocol layer** | **Application layer** | **"Mining pool"** | **"Hashers" (individual & collective)** | **Machine manufacturers (ASIC)** | **Full nodes** | **Wallets** | **Fund custody & payment** | **Exchanges** | **Data analysis services** | **Media & events** | **Consulting, training, and teaching** | **Other (app/Dapp, various projects)** | **Users (Users, Investors, traders)** |
| **1** | NO | YES | NO | YES | NO | YES | NO | NO | NO | NO | NO | YES | YES | YES |
| **2** | NO | YES | NO | YES | NO | YES | NO | NO | YES | NO | NO | NO | YES | YES |
| **3** | NO | YES | NO | NO | NO | YES | NO | NO | NO | YES | NO | NO | YES | YES |
| **4** | NO | YES | NO | NO | NO | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| **5** | YES | YES | NO | NO | YES | YES | YES | YES | YES | NO | NO | NO | YES | YES |
| **6** | NO | NO | NO | NO | NO | NO | NO | NO | YES | YES | YES | YES | YES | YES |
| **7** | NO | YES | NO | NO | NO | YES | YES | YES | YES | NO | NO | NO | YES | YES |
| **8** | NO | NO | NO | NO | NO | YES | NO | NO | NO | NO | YES | YES | NO | YES |
| **9** | NO | YES | NO | NO | NO | YES | YES | YES | YES | NO | YES | YES | YES | YES |
| **10** | NO | YES | NO | NO | YES | YES | YES | YES | YES | NO | YES | YES | YES | YES |
| **11** | YES | YES | NO | NO | NO | YES | NO | NO | NO | NO | NO | NO | YES | YES |
| **12** | YES | YES | NO | NO | NO | YES | NO | NO | NO | NO | NO | NO | YES | YES |
| **13** | NO | YES | NO | NO | NO | YES | NO | NO | NO | YES | YES | YES | YES | YES |
| **14** | NO | YES | NO | NO | NO | YES | NO | NO | NO | YES | YES | YES | YES | YES |
| **15** | NO | NO | NO | NO | NO | YES | NO | NO | NO | NO | YES | NO | YES | YES |
| **16** | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO | YES | NO | YES |
| **17** | NO | YES | NO | NO | NO | YES | YES | YES | YES | NO | NO | NO | YES | YES |
| **18** | NO | NO | NO | NO | NO | YES | NO | NO | YES | NO | YES | NO | NO | YES |
| **19** | NO | YES | NO | NO | NO | YES | NO | NO | NO | NO | YES | YES | YES | YES |
| **20** | NO | YES | NO | NO | NO | YES | NO | NO | NO | YES | NO | NO | NO | YES |

# Appendix V: Technical and computer-related annexes

## Appendix V.1: Asymmetric cryptography

| ![](media/image79.png) |
|---|

## Appendix V.2: Merkle Tree

| ![](media/image80.png) |
|---|

## Appendix V.3: Hash function

| ![](media/image81.png) |
|---|

## Appendix V.4: Simplified Payment Verification (SPV)

| ![](media/image82.png) |
|---|

## Appendix V.5: The 51% attack

| ![](media/image83.png) |
|---|
