# https://medium.freecodecamp.org/the-rise-of-the-data-engineer-91be18f1e603
# https://medium.com/@maximebeauchemin/heres-a-follow-up-interview-to-this-article-on-the-data-engineering-podcast-dd7397377d56?source=responses

'''
Like data scientists, data engineers write code.
They're highly analytical, and are interested in
data visualization.

Unlike data scientists - and inspired by our more
mature parent, software engineering - data engineers
build tools, infrastructure, frameworks, and services.
In fact, it's arguable that data engineering is much
closer to software engineering than it is to a data
science.

The data engineering field could be thought of as
a superset of business intelligence and data
warehousing that brings more elements from software
engineering. This discipline also integrates
specialization around the operation of so-called
'big data' distributed systems, along with concepts
around the extended Hadoop ecosystem, stream
processing, and in computation at scale.

In smaller companies - where no data infrastructure
team has yet been formalized - the data engineering
role may also cover the workload around setting up
and operating the organization's data infrastructure.
This includes tasks like setting up and operating
platforms like Hadoop/Hive/HBase, Spark, and the like.

While the engineering aspect of the role is growing
in scope, other aspects of the original business
engineering role are becoming secondary. Areas like
crafting and maintaining portfolios of reports and
dashboards are not a data engineer's primary focus.

We now have better self-service tooling where
analysts, data scientists, and the general
'information worker' is becoming more data-savvy
and can take care of data consumption autonomously.

ETL is Changing

The market is undergoing a general shift away from
drag-and-drop ETL tools towards a more programmatic
approach. Product know-how on platforms like
Informatica, IBM Datastage, Cognos, AbInitio or
Microsoft SSIS isn't common amongst data engineers,
and being replaced by more generic software
engineering skills along with understanding of
programmatic or configuration driven platforms
like Airflow, Oozie, Azkabhan, or Luigi. It's also
fairly common for enfineers to develop and manage
their own job orchestrator/scheduler.

There's a multitude of reasons why complex pieces
of software are not developed using drag-and-drop
tools: it's that ultimately CODE IS THE BEST
ABSTRACTION THERE IS FOR SOFTWARE. It's easy to
infer that these same reasons apply to writing
ETL as it applies to any other software. Code
allows for arbitrary levels of abstractions,
allows for all logical operation in a familiar way,
integrates well with source control, is easy to
version and to collaborate on. The fact that ETL
tools evolved to expose graphical interfaces seems
like a detour in the history of data processing.

Let's highlight the fact that the abstractions
exposed by traditional ETL tools are off-target.
Sure, there's a need to abstract the complexity
of data processing, computation and storage. But
I would argue that the solution is not to expose
ETL primitives (like source/target, aggregations,
filtering) into a drag-and-drop fashion. The
abstractions needed are of a higher level.

Data modeling is changing

Typical data modeling techniques - like the star
schema - which defined our approach to data
modeling for the analytics workloads typically
associated with data warehouses, are less relevant
than they once were. The traditional best practices
of data warehousing are losing ground on a shifting
stack. Storage and compute is cheaper than ever,
and with the advent of distributed databases that
scale out linearly, the scarcer resource is
engineering time.

Some changes observed in data modeling techniques:

    Further denormalization: maintaining surrogate
    keys in dimensions can be tricky, and it makes
    fact tables less readable. The use of natural,
    human-readable keys and dimension attributes in
    fact tables is becoming more common, reducing
    the need for costly joins that can be heavy on
    ditributed databases. Also note that support
    for encoding and compression in serialization
    formats like Parquet or ORC, or in database
    engines like Vertica, address most of the
    performance loss that would normally be
    associated with denormalization. Those systems
    have been taught to normalize the data for
    storage of their own.

    Blobs: modern databases have a growing support
    for blobs through native types and functions.
    This opens new moves in the data modeler's
    playbook, and can allow for fact tables to store
    multiple grains at once when needed

    Dynamic schemas: since the advent of map reduce,
    with the growing popularity of document stores
    and with support for blobs in databases, it's
    becoming easier to evolve database schemas
    without executing DML. This makes it easier to
    have an iterative approach to warehousing, and
    removes the need to get full consensus and
    buy-in prior to development.

    Systematically snapshotting dimensions (storing
    a full copy of the dimension for each ETL
    schedule cycle, usually in distinct table partitions)
    as a generic way to handle slowly changing
    dimension (SCD) is a simple generic approach that
    requires little engineering effort, and that
    unlike the classical approach, is easy to grasp
    when writing ETL and queries alike. It's also
    easy and relatively cheap to denormalize the
    dimension's attribute into the fact table to
    keep track of its value at the moment of the
    transaction. In retrospect, complex SCD modeling
    techniques are not intuitive and reduce
    accessibility.

    Conformance, as in conformed dimensions and
    metrics is still extremely important in
    modern data environment, but with the need
    for data warehouses to move fast, and with
    more team and roles invited to contribute to
    this effort, it's less imperative and more of
    a tradeoff. Consensus and convergence can
    happen as a background process in the areas
    where the pain point of divergence becomes
    out-of-hand.

Also, more generally, it's arguable to say that
with the commoditization of compute cycles and
with more people being data-savvy than before,
there's less need to precompute and store results
in the warehouse. For instance, you might can
have complex Spark jobs that can compute complex
analysis on-demand only, and not be scheduled to
be part of the warehouse.

ROLES & RESPONSIBILITIES

**The Data Warehouse**

"A data warehouse is a copy of transaction data
specifically structured for query analysis."
- Ralph Kimball

"A data warehouse is a subject-oriented,
integrated, time-variant and non-volatile
collection of data in support of management's
decision making process."
- Bill Inmon

The data engineer's focal point is the data
warehouse and gravitates around it.

The modern data warehouse is a more public
institution than it was historically, welcoming
data scientists, analysts, and software engineers
to partake in its construction and operation. Data
is simply too centric to the company's activity to
have limitation around what roles can manage its
flow.

The data engineering team will often own pockets
of certified, high quality areas in the data
warehouse. At Airbnb for instance, there's a set
of "core" schemas that are managed by the data
engineering team, where service level agreement
(SLAs) are clearly defined and measured, naming
conventions are strictly followed, business
metadata and documentation is of the highest
quality, and the related pipeline code follows
a set of well defined best practices.

Data engineers are also the "librarians" of the
data warehouse, cataloging and organizing metadata,
defining the processes by which one files or extract
data from the warehouse. In a fast-growing, rapidly
evolving, slightly chaotic data ecosystem, metadata
management and tooling become a vital component
of a modern data platform.

**Performance Tuning and Optimization**

Optimization is often coming from the perspective
of achieving more with the same amount of resources
or trying to linearize exponential growth in
resource utilization and costs.

**Data integration**

Data integration, the practice behind integrating
businesses and systems through the exchange of data,
is as important and as challenging as its ever
been. As Software as a Service (SaaS) becomes the
new standard way for companies to operate, the need
to synchronize referential data across these systems
becomes increasingly critical. Not only SaaS needs
up-to-date data to function, we often want to bring
the data generated on their side into our data
warehouse so that it can be analyzed along with
the rest of our data. Sure SaaS often have their
own analytics offering, but are systematically
lacking the perspective that the rest of your
company's data offer, so more often than not
it's necessary to pull some of this data back.

Letting these SaaS offerings redefine referential
data without integrating and sharing a common
primary key is a disaster that should be avoided
at all costs. No one wants to manually maintain
two employee or customer lists in two different
systems, and worst: having to do fuzzy matching
when bringing their HR data back into their
warehouse.

Worst, company executives often sign deals with
SaaS providers without really considering the
data integration challenges. The integration
workload is systematically downplayed by
vendors to facilitate their sales, and leaves
data engineers stuck doing unaccounted,
under-appreciated work. Let alone the fact
that typical SaaS APIs are often poorly
designed, unclearly documented, and 'agile';
meaning that you can expect them to change
without notice.

**Services**

Data engineers are operating at a higher level of
abstraction and in some cases that means providing
services and tooling to automate the type of work
that data engineers, data scientists, or analysts
may do manually.

A few examples of services that data engineers and
data infrastructure engineers may build and operate:
    - data ingestion: services and tooling around
    'scraping' databases, loading logs, fetching
    data from external stores or APIs, etc.
    - metric computation: frameworks to compute and
    summarize engagement, growth or segmentation-
    related metrics
    - anomaly detection: automating data consumption
    to alert people when anomalous events occur or
    when trends are changing significantly
    - metadata management: tooling around allowing
    generation and consumption of metadata, making
    it easy to find information in and around the
    data warehouse
    -experimentation: A/B testing and experimentation
    frameworks are often critical pieces of a
    company's analytics with a significant data
    engineering component to it
    - instrumentation: analytics starts with logging
    events and attributes related to those events,
    data engineers have vested interests in making
    sure that high quality data is captured upstream
    -sessionization: pipelines that are specialized
    in understanding series of actions in time,
    allowing analysts to understand user behaviors

REQUIRED SKILLS

**SQL Mastery**

SQL is the language of data. A data engineer should
be able to express any degree of complexity in SQL
using techniques like 'correlated subqueries' and
window functions. SQL/DML/DDL primitives are simple
enough that it should hold no secrets to a data
engineer. Beyond the declarative nature of SQL,
the data engineer should be able to read and
understand database execution plans, and have an
understanding of what all the steps are, how indices
work, the different join algorithms and the
distributed dimension within the plan.

**Data Modeling Techniques**

Entity-relationship modeling should be a cognitive
reflex, along with a clear understanding of
normalization, and have a sharp intuition around
denormalization tradeoffs. The data engineer should
be familiar with dimensional modeling and the
related concepts and lexical field.

**ETL Design**

Writing efficient, resilient and 'evolvable' ETL
is key. (see associated blog post)

**Architectural Projections**

Like any professional in any given field of expertise,
the data engineer needs to have a high level
understanding of most of the tools, platforms,
libraries and other resources at their disposal.
The properties, use-cases and subtleties behind the
different flavors of databases, computation engines,
stream processors, message queues, workflow
orchestrators, serialization formats and other
related technologies.
